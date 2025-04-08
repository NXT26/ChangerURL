from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .models import URL, ClickLog
from typing import Optional
from datetime import timedelta, datetime


async def get_url_by_code(db: AsyncSession, code:str)-> Optional[URL]:
    result  = await db.execute(select(URL).where(URL.short_code == code))
    return result.scalar_one_or_none()

async def create_short_url(db: AsyncSession, short_code: str, target_url: str, expire_seconds: Optional[int] = None):
    expires_at = None
    if expire_seconds:
        expires_at = datetime.utcnow() + timedelta(seconds=expire_seconds)

    new_url = URL(short_code=short_code, target_url=target_url, expires_at=expires_at)
    db.add(new_url)
    await db.commit()
    await db.refresh(new_url)
    return new_url

async def increment_clicks(db:AsyncSession, code: str):
    await db.execute(
        update(URL)
        .where(URL.short_code == code)
        .values(clicks = URL.clicks +1)
    )
    await db.commit()

async def get_click_stats(db: AsyncSession, code: str ) -> Optional[dict]:
    url = await get_url_by_code(db,code)
    if url:
        return {
            "url": url.target_url,
            "clicks": url.clicks,
            "expires_at": url.expires_at.isoformat() if url.expires_at else None
        }
    return None

async def deactivate_url(db: AsyncSession, code: str):
    await db.execute(
        update(URL)
        .where(URL.short_code == code)
        .values(is_active=False)
    )
    await db.commit()

async def log_click(db: AsyncSession, short_code: str):
    log = ClickLog(short_code=short_code)
    db.add(log)
    await db.commit()




