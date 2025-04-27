import httpx
import pytest
from httpx import AsyncClient,ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_shorten_url():
    async with AsyncClient(
        base_url="http://test",
        transport=httpx.ASGITransport(app=app)
    ) as ac:
        response = await ac.post("/api/shorten", json={"target_url": "https://example.com"})
    assert response.status_code == 200
    assert "short_url" in response.json()

@pytest.mark.asyncio
async def test_redirect():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/shorten", json={"target_url": "https://example.com"})
        assert response.status_code == 200
        short_url = response.json()["short_url"]
        code = short_url.rsplit("/", 1)[-1]

        redirect_response = await ac.get(f"/{code}", follow_redirects=False)
        assert redirect_response.status_code == 307
        assert redirect_response.headers["location"].rstrip("/") == "https://example.com"

@pytest.mark.asyncio
async def test_create_with_custom_code():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        custom_code = "mycustom"
        response = await ac.post("/api/shorten", json={
            "target_url": "https://example.com",
            "custom_code": custom_code
        })
        assert response.status_code == 200
        assert response.json()["short_url"].endswith(f"/{custom_code}")

@pytest.mark.asyncio
async def test_custom_code_conflict():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        custom_code = "duplicatecode"
        # Первая вставка
        await ac.post("/api/shorten", json={
            "target_url": "https://example.com",
            "custom_code": custom_code
        })
        # Повторная вставка
        response = await ac.post("/api/shorten", json={
            "target_url": "https://another.com",
            "custom_code": custom_code
        })
        assert response.status_code == 409

@pytest.mark.asyncio
async def test_stats_click_count():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/shorten", json={"target_url": "https://example.com"})
        short_url = response.json()["short_url"]
        code = short_url.rsplit("/", 1)[-1]

        # Один клик
        await ac.get(f"/{code}")

        # Проверка статистики
        stats = await ac.get(f"/stats/{code}")
        assert stats.status_code == 200
        assert stats.json()["clicks"] == 1

@pytest.mark.asyncio
async def test_redirect_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/nonexistent", follow_redirects=False)
        assert response.status_code == 404
