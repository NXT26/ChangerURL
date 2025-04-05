from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .models import URL
from typing import Optional

async def get_url_by_code(db: AsyncSession, code:str)-> Optional[URL]:
    result  = await db.execute(select(URL).where(URL.short_code == code))
    return result.scalar_one_or_none()

async def create_short_url(db: AsyncSession, short_code: str, target_url: str):
    new_url = URL(short_code=short_code, target_url=target_url)
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
        return {"url": url.target_url, "clicks": url.clicks}
    return None

async def deactivate_url(db: AsyncSession, code: str):
    await db.execute(
        update(URL)
        .where(URL.short_code == code)
        .values(is_active=False)
    )
    await db.commit()




