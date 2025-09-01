"""Redis cache utilities"""

from typing import Optional

import redis.asyncio as aioredis

from app.core.config import settings

_redis_client: Optional[aioredis.Redis] = None


def get_redis() -> Optional[aioredis.Redis]:
    """Return a shared asyncio Redis client or None if connection fails."""
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                max_connections=20,
                retry_on_timeout=True,
                health_check_interval=30,
            )
        except Exception:
            _redis_client = None
    return _redis_client


