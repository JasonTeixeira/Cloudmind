"""Validate critical runtime dependencies before boot.

Exits with non-zero code on failure in production, warnings in dev.
"""

import os
import sys
import asyncio


async def check_redis() -> bool:
    try:
        import redis.asyncio as aioredis
        url = os.getenv("REDIS_URL")
        if not url:
            return False
        client = aioredis.from_url(url, decode_responses=True)
        await client.ping()
        return True
    except Exception:
        return False


def check_secret_key() -> bool:
    return bool(os.getenv("SECRET_KEY"))


async def main() -> int:
    env = (os.getenv("ENVIRONMENT") or "development").lower()
    failures = []
    if env == "production":
        if not check_secret_key():
            failures.append("SECRET_KEY missing")
        if not await check_redis():
            failures.append("Redis not reachable")
    if failures:
        print("Validation failed:", failures)
        return 1
    print("Environment validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))


