import asyncio
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import init_db, get_db, SessionLocal, Conversation, Message
from app.redis_client import get_redis, CHAT_CHANNEL
from app.agents import ALL_AGENTS
from app.conversation_manager import start_conversation
from app.scripts import TOPICS
from app.ws_manager import manager

background_tasks: list[asyncio.Task] = []


async def redis_broadcaster():
    """
    Yeh FastAPI ka apna Redis subscriber hai.
    Ye har message ko:
      1. Database me save karta hai (permanent history)
      2. Connected browser clients ko WebSocket se turant bhejta hai
    """
    r = get_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(CHAT_CHANNEL)

    async for message in pubsub.listen():
        if message["type"] != "message":
            continue
        try:
            data = json.loads(message["data"])
        except (TypeError, ValueError):
            continue

        if data.get("event") == "message":
            db: Session = SessionLocal()
            try:
                db.add(
                    Message(
                        conversation_id=data["conversation_id"],
                        speaker=data["speaker"],
                        text=data["text"],
                        turn=data["turn"],
                    )
                )
                db.commit()
            finally:
                db.close()
            await manager.broadcast(data)

        elif data.get("event") == "end":
            db: Session = SessionLocal()
            try:
                conv = db.query(Conversation).get(data["conversation_id"])
                if conv:
                    conv.status = "finished"
                    db.commit()
            finally:
                db.close()
            await manager.broadcast(data)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    # Dono agents ko background me chalao - ye hamesha CHAT_CHANNEL sunte rehte hain
    for agent in ALL_AGENTS:
        background_tasks.append(asyncio.create_task(agent.run()))
    background_tasks.append(asyncio.create_task(redis_broadcaster()))
    yield
    for t in background_tasks:
        t.cancel()


app = FastAPI(title="Signal Exchange - AI Agent Collaboration", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/topics")
def list_topics():
    return [
        {"key": k, "title": v["title"], "description": v["description"]}
        for k, v in TOPICS.items()
    ]


@app.post("/api/conversations/start")
async def api_start_conversation(topic_key: str = None, db: Session = Depends(get_db)):
    conversation = await start_conversation(db, topic_key)
    return {
        "conversation_id": conversation.id,
        "topic_key": conversation.topic_key,
        "topic_title": conversation.topic_title,
    }


@app.get("/api/conversations/{conversation_id}/messages")
def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.turn.asc())
        .all()
    )
    return [
        {"speaker": m.speaker, "text": m.text, "turn": m.turn, "created_at": m.created_at}
        for m in msgs
    ]


@app.get("/api/conversations")
def list_conversations(db: Session = Depends(get_db)):
    convs = db.query(Conversation).order_by(Conversation.id.desc()).limit(20).all()
    return [
        {
            "id": c.id,
            "topic_key": c.topic_key,
            "topic_title": c.topic_title,
            "status": c.status,
            "created_at": c.created_at,
        }
        for c in convs
    ]


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep-alive ping
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Frontend serve karne ke liye (index.html)
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
