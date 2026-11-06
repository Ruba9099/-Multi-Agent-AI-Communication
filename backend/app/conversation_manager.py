import json

from sqlalchemy.orm import Session

from .database import Conversation
from .redis_client import get_redis, CHAT_CHANNEL
from .scripts import TOPICS, DEFAULT_TOPIC


async def start_conversation(db: Session, topic_key: str | None = None) -> Conversation:
    if topic_key not in TOPICS:
        topic_key = DEFAULT_TOPIC

    topic = TOPICS[topic_key]
    conversation = Conversation(
        topic_key=topic_key, topic_title=topic["title"], status="running"
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    # Turn 0 hamesha "innovator" ki opening line hoti hai (script se).
    speaker, text = topic["script"][0]

    r = get_redis()
    payload = {
        "event": "message",
        "conversation_id": conversation.id,
        "topic_key": topic_key,
        "speaker": speaker,
        "text": text,
        "turn": 0,
    }
    await r.publish(CHAT_CHANNEL, json.dumps(payload))

    return conversation
