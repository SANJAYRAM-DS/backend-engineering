import logging
from typing import Optional
import redis.asyncio as aioredis
from src.core.config import settings

logger = logging.getLogger("url_shortener")

_redis_client: Optional[aioredis.Redis] = None


async def get_redis_client() -> Optional[aioredis.Redis]:
    """Returns async redis client if available, or None if unavailable."""
    global _redis_client
    if _redis_client is not None:
        return _redis_client

    try:
        url = settings.assemble_redis_url()
        client = aioredis.from_url(url, encoding="utf-8", decode_responses=True, socket_connect_timeout=1.0)
        await client.ping()
        _redis_client = client
        return _redis_client
    except Exception as e:
        logger.warning(f"Redis connection failed ({e}). Operating in cache-disabled fallback mode.")
        return None


async def close_redis_client() -> None:
    global _redis_client
    if _redis_client is not None:
        try:
            await _redis_client.close()
        except Exception:
            pass
        _redis_client = None
