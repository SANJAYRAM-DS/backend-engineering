from typing import Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis
from src.db.session import get_db
from src.core.redis import get_redis_client
from src.services.url_service import URLService


async def get_redis_dep() -> Optional[aioredis.Redis]:
    return await get_redis_client()


async def get_url_service(
    db: AsyncSession = Depends(get_db),
    redis: Optional[aioredis.Redis] = Depends(get_redis_dep),
) -> URLService:
    return URLService(db=db, redis=redis)