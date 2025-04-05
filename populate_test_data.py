import httpx
import random
import string
import asyncio

API_URL = "http://localhost:8000/api/shorten"


DOMAINS = [
    "google.com", "youtube.com", "github.com", "docs.python.org",
    "openai.com", "wikipedia.org", "nytimes.com", "stackoverflow.com",
    "fastapi.tiangolo.com", "reddit.com"
]

def random_url():
    domain = random.choice(DOMAINS)
    path = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5, 12)))
    return f"https://{domain}/{path}"

def random_custom_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

async def generate_links(count=30):
    async with httpx.AsyncClient() as client:
        for i in range(count):

            if i % 2 == 0:
                data = {
                    "target_url": random_url(),
                    "custom_code": random_custom_code()
                }
            else:
                data = {
                    "target_url": random_url()
                }

            response = await client.post(API_URL, json=data)
            if response.status_code == 200:
                print(f"[{i+1}] ✅ {response.json()['short_url']}")
            else:
                print(f"[{i+1}] ❌ {response.status_code} — {response.text}")

if __name__ == "__main__":
    asyncio.run(generate_links())

