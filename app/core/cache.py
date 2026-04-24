import json
import logging
from typing import Any
from datetime import datetime
import redis

from app.core.config import settings

logger = logging.getLogger(__name__)

redis_client: redis.Redis | None = None


def serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def get_redis() -> redis.Redis:
    "Return (or create) the shared async Redis client."
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return redis_client


def cache_get(key: str) -> Any | None:
    "Return deserialized value, or None on miss/error."
    try:
        client = get_redis()
        value = client.get(key)
        if value is None:
            return None
        return json.loads(value)
    except Exception:
        logger.warning("cache_get failed for key=%s", key, exc_info=True)
        return None


def cache_set(key: str, value: Any, ttl: int = 60) -> None:
    "Serialize and store value with TTL in seconds."
    try:
        client = get_redis()
        client.set(key, json.dumps(value, default=serialize), ex=ttl)
    except Exception:
        logger.warning("cache_set failed for key=%s", key, exc_info=True)


def cache_delete_pattern(pattern: str) -> None:
    "Delete all keys matching a pattern, e.g. 'tasks:org:42:*'."
    try:
        client = get_redis()
        keys = client.keys(pattern)
        if keys:
            client.delete(*keys)
            logger.debug("Invalidated %d keys for pattern=%s", len(keys), pattern)
    except Exception:
        logger.warning("cache_delete_pattern failed for pattern=%s", pattern, exc_info=True)