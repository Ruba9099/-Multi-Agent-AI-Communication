# 🔴 Signal Exchange — AI Agent Collaboration

## 🧠 (Architecture)

```
┌─────────────┐   publish    ┌───────────────┐   subscribe   ┌──────────────┐
│  Innovator   │ ───────────▶│  Redis Channel │◀───────────── │   Reviewer    │
│    Agent     │◀─────────── │ chat:conversation│──────────▶  │    Agent      │
└─────────────┘   subscribe  └───────┬────────┘   publish     └──────────────┘
                                      │ subscribe
                                      ▼
                              ┌───────────────┐
                              │ FastAPI Server │
                              │ (broadcaster)  │
                              └───────┬────────┘
                        save to DB    │    push over WebSocket
                              ┌───────┴────────┐
                              ▼                ▼
                        ┌──────────┐    ┌─────────────┐
                        │ SQLite DB │    │ Browser UI  │
                        │ (history) │    │ (live chat) │
                        └──────────┘    └─────────────┘
```

- **Innovator Agent** aur **Reviewer Agent** both independently Redis channel `chat:conversation`  **subscribe** 
- when agent a message **publish** , second agent Immediately listen and reply **publish**  — this is real  **Pub/Sub pattern** 
- FastAPI server is a sucriber of this channel  — every message **SQLite database** save and through **WebSocket** reach to  browser immediately.
- Frontend  live "chat console"  show real-time conversation of both agents.

## 📁 Project Structure

```
chatbot-project/
├── backend/
│   ├── main.py                  # FastAPI app + WebSocket + Redis broadcaster
│   ├── requirements.txt
│   └── app/
│       ├── agents.py            # Innovator & Reviewer agent classes (pub/sub logic)
│       ├── conversation_manager.py  # new conversation start karta hai
│       ├── database.py          # SQLAlchemy models (Conversation, Message)
│       ├── redis_client.py      # Redis connection + channel name
│       └── scripts.py           # Topic content bank (3 topics)
└── frontend/
    └── index.html               # Live chat UI (vanilla JS + WebSocket)
```

- **Full-stack**: FastAPI backend + WebSocket + SQLite database + live frontend.
- **Multi-agent AI concept**
  

---
Made with FastAPI, Redis, SQLAlchemy & WebSockets.
