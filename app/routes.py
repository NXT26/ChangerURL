from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_session
from .metrics import track_time, REQUEST_TIME, QR_CODE_GENERATION_TIME
import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse
from .crud import (
    get_url_by_code,
    create_short_url,
    increment_clicks,
    get_click_stats, deactivate_url, log_click
)
from .models import URLItem
import re
import random
import string

router = APIRouter()

def generate_short_code(length: int = 6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@track_time(QR_CODE_GENERATION_TIME)
def generate_qr_code(url: str):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


@router.post("/api/shorten")
@track_time(REQUEST_TIME)
async def shorten_url(item: URLItem, db: AsyncSession = Depends(get_session)):
    code = item.custom_code or generate_short_code()

    if not re.fullmatch(r"[a-zA-Z0-9]{3,20}", code):
        raise HTTPException(status_code=422, detail="Код должен содержать только буквы и цифры и быть от 3 до 20 символов")

    existing = await get_url_by_code(db, code)
    if existing:
        raise HTTPException(status_code=409, detail="Код уже занят")

    await create_short_url(db, code, str(item.target_url), item.expire_seconds)

    return {"short_url": f"http://localhost:8000/{code}"}


@router.get("/{code}")
async def redirect_url_code(code: str, db: AsyncSession = Depends(get_session)):
    url = await get_url_by_code(db, code)

    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    if url.expires_at and url.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Срок действия ссылки истёк")

    await increment_clicks(db, code)
    await log_click(db, code)
    return RedirectResponse(url=url.target_url)


@router.get("/stats/{code}")
async def get_status(code: str, db: AsyncSession = Depends(get_session)):
    stats = await get_click_stats(db, code)
    if not stats:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
    return stats


@router.post("/api/deactivate/{code}")
async def deactivate(code: str, db: AsyncSession = Depends(get_session)):
    url = await get_url_by_code(db, code)
    if not url:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")

    if not url.is_active:
        return {"message": "Ссылка уже неактивна"}

    await deactivate_url(db, code)
    return {"message": f"Ссылка {code} успешно деактивирована"}

@router.get("/qr/{code}")
async def get_qr(code: str, db: AsyncSession = Depends(get_session)):
    url = await get_url_by_code(db, code)
    if not url:
        raise HTTPException(status_code=404, detail="Код не найден")

    short_url = f"http://localhost:8000/{url.short_code}"
    qr_image = generate_qr_code(short_url)
    return StreamingResponse(qr_image, media_type="image/png")
