import datetime
from typing import Optional
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.db.models import URL, ClickEvent


class URLRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_short_code(
        self, short_code: str, include_inactive: bool = False
    ) -> Optional[URL]:
        query = select(URL).where(URL.short_code == short_code)
        if not include_inactive:
            query = query.where(URL.is_active == True)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_url(
        self,
        short_code: str,
        original_url: str,
        expires_at: Optional[datetime.datetime] = None,
        user_id: Optional[str] = None,
    ) -> URL:
        url_obj = URL(
            short_code=short_code,
            original_url=original_url,
            expires_at=expires_at,
            user_id=user_id,
        )
        self.db.add(url_obj)
        await self.db.commit()
        await self.db.refresh(url_obj)
        return url_obj

    async def increment_click_count(self, short_code: str) -> None:
        await self.db.execute(
            update(URL)
            .where(URL.short_code == short_code)
            .values(click_count=URL.click_count + 1)
        )
        await self.db.commit()

    async def log_click_event(
        self,
        short_code: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        referrer: Optional[str] = None,
    ) -> None:
        click_obj = ClickEvent(
            short_code=short_code,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
        )
        self.db.add(click_obj)
        await self.db.commit()

    async def deactivate_url(self, short_code: str) -> bool:
        result = await self.db.execute(
            update(URL)
            .where(URL.short_code == short_code, URL.is_active == True)
            .values(is_active=False)
        )
        await self.db.commit()
        return result.rowcount > 0