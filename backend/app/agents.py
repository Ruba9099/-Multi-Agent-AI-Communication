import asyncio
import json
import random

from .redis_client import get_redis, CHAT_CHANNEL
from .scripts import TOPICS


class Agent:
    """
    Ek Agent apne aap ek independent 'listener' hai.
    - Yeh CHAT_CHANNEL par subscribe karta hai.
    - Jab dusre agent ka message aata hai, yeh check karta hai
      ke script me agla turn iska (is agent ka) hai ya nahi.
    - Agar haan, to (typing simulate karke) apna reply publish karta hai.

    NOTE FOR FUTURE UPGRADE (real LLM):
    Abhi text `scripts.py` ki fixed script se aata hai taake
    conversation hamesha meaningful/coherent rahe bina kisi API key ke.
    Agar aap isko REAL LLM se chalana chahti hain (Claude/GPT etc),
    to bas `generate_reply_text()` function ko replace karke wahan
    apna API call daal dein - baaki poora pub/sub architecture waisa
    ka waisa reh sakta hai.
    """

    def __init__(self, name: str):
        self.name = name

    async def run(self):
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

            if data.get("event") != "message":
                continue
            if data.get("speaker") == self.name:
                continue  # apna hi echo ignore karo

            await self._maybe_reply(data)

    async def _maybe_reply(self, data: dict):
        topic_key = data["topic_key"]
        conversation_id = data["conversation_id"]
        next_turn = data["turn"] + 1

        script = TOPICS[topic_key]["script"]
        if next_turn >= len(script):
            return  # conversation already khatam ho chuki

        speaker, text = script[next_turn]
        if speaker != self.name:
            return  # abhi meri baari nahi hai

        # "typing..." jaisa realistic delay
        await asyncio.sleep(random.uniform(1.5, 3.0))

        text = generate_reply_text(speaker, text)

        r = get_redis()
        payload = {
            "event": "message",
            "conversation_id": conversation_id,
            "topic_key": topic_key,
            "speaker": self.name,
            "text": text,
            "turn": next_turn,
        }
        await r.publish(CHAT_CHANNEL, json.dumps(payload))

        if next_turn == len(script) - 1:
            await asyncio.sleep(1.0)
            await r.publish(
                CHAT_CHANNEL,
                json.dumps({"event": "end", "conversation_id": conversation_id}),
            )


def generate_reply_text(speaker: str, scripted_text: str) -> str:
    """
    Yahi woh single function hai jise replace karke aap real LLM
    (Anthropic API, etc.) laga sakti hain. Abhi yeh scripted text
    seedha return karta hai.
    """
    return scripted_text


INNOVATOR = Agent("innovator")
REVIEWER = Agent("reviewer")
ALL_AGENTS = [INNOVATOR, REVIEWER]
