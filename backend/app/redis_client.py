import redis.asyncio as redis

REDIS_URL = "redis://localhost:6379/0"

# Yeh Redis Pub/Sub ka main channel hai. Dono agents aur FastAPI
# is channel par publish/subscribe karte hain.
CHAT_CHANNEL = "chat:conversation"

_redis_pool = None


def get_redis():
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = redis.from_url(REDIS_URL, decode_responses=True)
    return _redis_pool
