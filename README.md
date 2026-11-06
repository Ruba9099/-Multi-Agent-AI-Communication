# 🔴 Signal Exchange — AI Agent Collaboration

Yeh project ek **portfolio-ready** demo hai jisme do AI agents (**Innovator** aur **Reviewer**) Redis Pub/Sub ke zariye aapas me ek naye AI/Tech topic par healthy discussion karte hain — pros/cons discuss karte hain — aur yeh saari conversation **live web browser** me dikhti hai.

## 🧠 Yeh kaise kaam karta hai (Architecture)

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

- **Innovator Agent** aur **Reviewer Agent** dono independently Redis channel `chat:conversation` ko **subscribe** karte hain.
- Jab ek agent apna message **publish** karta hai, dusra agent usko turant "sunta" hai aur apni turn par reply **publish** karta hai — yehi asli **Pub/Sub pattern** hai.
- FastAPI server bhi isi channel ka ek subscriber hai — har message ko **SQLite database** me save karta hai aur **WebSocket** ke zariye browser tak turant pahunchata hai.
- Frontend ek live "chat console" hai jo real-time me dono agents ki baat-cheet dikhata hai.

## 📁 Project Structure

```
chatbot-project/
├── backend/
│   ├── main.py                  # FastAPI app + WebSocket + Redis broadcaster
│   ├── requirements.txt
│   └── app/
│       ├── agents.py            # Innovator & Reviewer agent classes (pub/sub logic)
│       ├── conversation_manager.py  # naya conversation start karta hai
│       ├── database.py          # SQLAlchemy models (Conversation, Message)
│       ├── redis_client.py      # Redis connection + channel name
│       └── scripts.py           # Topic content bank (3 topics diye gaye hain)
└── frontend/
    └── index.html               # Live chat UI (vanilla JS + WebSocket)
```

## ⚙️ Setup (apne computer par)

### 1. Redis install karein
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
redis-server --daemonize yes

# Mac
brew install redis
brew services start redis
```

### 2. Python dependencies install karein
```bash
cd backend
pip install -r requirements.txt
```

### 3. Server run karein
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### 4. Browser me kholein
```
http://localhost:8000
```

Topic select karein, **"Start Conversation"** dabayein, aur dekhein dono agents live baat-cheet karte hue!

## 🎯 Topics jo already diye gaye hain

1. **Agentic AI & Multi-Agent Systems** ⭐ (portfolio ke liye best — kyunki yeh khud is project ka bhi concept hai!)
2. **Retrieval-Augmented Generation (RAG)**
3. **On-Device / Edge AI**

Aap `backend/app/scripts.py` file me naye topics bhi easily add kar sakti hain — bas isi format me `(speaker, text)` tuples ki list bana dein.

## 🚀 Ise real LLM se upgrade kaise karein (optional, future step)

Abhi conversations pre-written "script" se chalti hain taake project bina kisi paid API key ke turant chal sake, aur conversation hamesha meaningful rahe.

Agar aap chahen ke agents **real-time** apne aap (Claude/GPT jaisi API se) jawab generate karein, to sirf ek jagah change karni hai:

`backend/app/agents.py` me `generate_reply_text()` function — usme apna LLM API call daal dein. Baaki poora Redis Pub/Sub + WebSocket + Database architecture waisa hi rahega.

## 💼 Portfolio ke liye kyun best hai

- **Real-world backend pattern**: Pub/Sub messaging (Redis) — jo bade distributed systems (microservices, notifications, chat apps) me use hota hai.
- **Full-stack**: FastAPI backend + WebSocket + SQLite database + live frontend.
- **Multi-agent AI concept**: aaj ke AI industry ka sabse hot topic (agentic systems).
- Aap README me yeh diagram aur explanation seedha use kar sakti hain apne resume/portfolio ke description ke liye.

---
Made with FastAPI, Redis, SQLAlchemy & WebSockets.
