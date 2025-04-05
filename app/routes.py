from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from .db import async_session, get_session
from .crud import (
    get_url_by_code,
    create_short_url,
    increment_clicks,
    get_click_stats
)
from .models import URLItem
import re
import random
import string

router = APIRouter()

def generate_short_code(length: int = 6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@router.post("/api/shorten")
async def shorten_url(item: URLItem, db: AsyncSession = Depends(get_session)):
    code = item.custom_code or generate_short_code()

    if not re.fullmatch(r"[a-zA-Z0-9]{3,20}", code):
        raise HTTPException(status_code=422, detail="Код должен содержать только буквы и цифры и быть от 3 до 20 символов")

    existing = await get_url_by_code(db, code)
    if existing:
        raise HTTPException(status_code=409, detail="Код уже занят")

    await create_short_url(db, code, str(item.target_url))

    return {"short_url": f"http://localhost:8000/{code}"}


@router.get("/{code}")
async def redirect_url_code(code: str, db: AsyncSession = Depends(get_session)):
    url = await get_url_by_code(db, code)

    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    await increment_clicks(db, code)
    return RedirectResponse(url=url.target_url)


@router.get("/stats/{code}")
async def get_status(code: str, db: AsyncSession = Depends(get_session)):
    stats = await get_click_stats(db, code)
    if not stats:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
    return stats
