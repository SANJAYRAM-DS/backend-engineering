import datetime
import logging
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import redis.asyncio as aioredis

from src.repositories.url_repository import URLRepository
from src.services.base62 import encode_base62
from src.services.snowflake import SnowflakeIDGenerator
from src.schemas.url import URLCreateRequest, URLResponse, AnalyticsResponse
from src.core.config import settings

logger = logging.getLogger("url_shortener")

# Initialize global Snowflake generator for this worker instance
snowflake_gen = SnowflakeIDGenerator(
    worker_id=settings.WORKER_ID, datacenter_id=settings.DATACENTER_ID
)


class URLService:
    def __init__(
        self, db: AsyncSession, redis: Optional[aioredis.Redis] = None
    ):
        self.repo = URLRepository(db)
        self.redis = redis

    async def create_short_url(self, request: URLCreateRequest) -> URLResponse:
        if request.custom_alias:
            existing = await self.repo.get_by_short_code(
                request.custom_alias, include_inactive=True
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Custom alias '{request.custom_alias}' is already taken.",
                )
            short_code = request.custom_alias
        else:
            # Generate Snowflake ID and convert to Base62
            max_attempts = 5
            short_code = ""
            for attempt in range(max_attempts):
                sf_id = snowflake_gen.generate_id()
                candidate_code = encode_base62(sf_id)[:7]
                existing = await self.repo.get_by_short_code(
                    candidate_code, include_inactive=True
                )
                if not existing:
                    short_code = candidate_code
                    break
            if not short_code:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to generate unique short code.",
                )

        try:
            url_record = await self.repo.create_url(
                short_code=short_code,
                original_url=request.original_url,
                expires_at=request.expires_at,
            )
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Short code '{short_code}' already exists.",
            )

        # Cache-Aside: Pre-warm Redis cache if redis is available
        if self.redis:
            try:
                cache_key = f"url:{short_code}"
                ttl = 3600
                if request.expires_at:
                    now = datetime.datetime.now(datetime.timezone.utc)
                    remaining = int((request.expires_at - now).total_seconds())
                    if remaining > 0:
                        ttl = min(ttl, remaining)
                await self.redis.set(cache_key, url_record.original_url, ex=ttl)
            except Exception as e:
                logger.warning(f"Failed to cache new short URL in Redis: {e}")

        return URLResponse(
            short_code=url_record.short_code,
            short_url=f"{settings.BASE_URL}/{url_record.short_code}",
            original_url=url_record.original_url,
            created_at=url_record.created_at,
            expires_at=url_record.expires_at,
            click_count=url_record.click_count,
            is_active=url_record.is_active,
        )

    async def resolve_url(
        self,
        short_code: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        referrer: Optional[str] = None,
    ) -> str:
        cache_key = f"url:{short_code}"
        original_url: Optional[str] = None

        # 1. Check Redis Cache
        if self.redis:
            try:
                cached = await self.redis.get(cache_key)
                if cached:
                    original_url = cached
            except Exception as e:
                logger.warning(f"Redis lookup failed: {e}")

        # 2. Cache Miss: Fallback to PostgreSQL
        if not original_url:
            record = await self.repo.get_by_short_code(short_code)
            if not record:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Short code '{short_code}' not found.",
                )

            if record.expires_at:
                now = datetime.datetime.now(datetime.timezone.utc)
                exp = record.expires_at
                if exp.tzinfo is None:
                    exp = exp.replace(tzinfo=datetime.timezone.utc)
                if exp < now:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Short code '{short_code}' has expired.",
                    )

            original_url = record.original_url

            # Populate Cache
            if self.redis:
                try:
                    await self.redis.set(cache_key, original_url, ex=3600)
                except Exception as e:
                    logger.warning(f"Redis set failed: {e}")

        # 3. Log click telemetry asynchronously in DB
        try:
            await self.repo.increment_click_count(short_code)
            await self.repo.log_click_event(
                short_code=short_code,
                ip_address=ip_address,
                user_agent=user_agent,
                referrer=referrer,
            )
        except Exception as e:
            logger.error(f"Failed to record click telemetry for '{short_code}': {e}")

        return original_url

    async def get_analytics(self, short_code: str) -> AnalyticsResponse:
        record = await self.repo.get_by_short_code(short_code)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Short code '{short_code}' not found.",
            )

        return AnalyticsResponse(
            short_code=record.short_code,
            original_url=record.original_url,
            total_clicks=record.click_count,
            created_at=record.created_at,
            expires_at=record.expires_at,
            is_active=record.is_active,
        )

    async def delete_url(self, short_code: str) -> bool:
        record = await self.repo.get_by_short_code(short_code)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Short code '{short_code}' not found.",
            )

        deactivated = await self.repo.deactivate_url(short_code)

        if self.redis:
            try:
                await self.redis.delete(f"url:{short_code}")
            except Exception as e:
                logger.warning(f"Failed to invalidate cache key url:{short_code}: {e}")

        return deactivated