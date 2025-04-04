from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from .models import URLItem
from fastapi import Request
from fastapi.responses import HTMLResponse
from .db_json import url_db, generate_short_code, save_db
import re
from fastapi import Form
from fastapi.templating import Jinja2Templates




router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def root():
    return {"message": "Доброе утро, пора писать укорачиватель"}

@router.get("/{code}")
async def redirect_url_code(code: str):
    item = url_db.get(code)

    if not item:
        raise HTTPException(status_code=404, detail="Short URL not found")
    item["clicks"] += 1
    save_db()
    return RedirectResponse(url=item["url"])


@router.post("/api/shorten")
async def shorten_url(item: URLItem, ):
    if item.custom_code:
        code = item.custom_code
        if not re.fullmatch(r"[a-zA-Z0-9]{3,20}", code):
            raise HTTPException(
                status_code=422,
                detail="Код должен содержать только буквы и цифры и быть от 3 до 20 символов"
            )
        if code in url_db:
            raise HTTPException(status_code=409, detail="Кажется этот код уже занят")
    else:
        code = generate_short_code()

        while code in url_db:
            code = generate_short_code()

    url_db[code] = {
        "url": item.target_url,
        "clicks": 0
    }

    save_db()

    return {"short_url": f"http://localhost:8000/{code}"}

@router.post("/shorten")
async def process_form(
        request: Request,
        target_url: str = Form(...),
        custom_code: str = Form(None)
):
    code = custom_code if custom_code else generate_short_code()

    if custom_code:
        if not re.fullmatch(r"[a-zA-Z0-9]{3,20}", custom_code):
            return templates.TemplateResponse("form.html", {
                "request": request,
                "error": "Код должен содержать только буквы и цифры и быть от 3 до 20 символов"
            })
        if code in url_db:
            return templates.TemplateResponse("form.html",{
                "request": request,
                "error": "Этот код уже занят"
            })
    else:
        while code in url_db:
            code = generate_short_code()

    url_db [code] ={
        "url": target_url,
        "clicks":0
    }
    save_db()

    short_url = f"http://localhost:8000/{code}"

    return templates.TemplateResponse("form.html",{
        "request": request,
        "short_url": short_url
    })


@router.get("/stats/{code}")
async def get_status(code: str):
    item = url_db.get(code)
    if not item:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return {"url": item["url"], "clicks": item["clicks"]}


@router.get("/shorten", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})
