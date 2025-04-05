import httpx
import asyncio
import random


BASE_URL = "http://localhost:8000"

CODES = [
    "youtube", "9AtO7k", "MkwHwX", "taQbmP", "ukpXUe", "GX85sA", "RhlwtA", "XZT4wI",
    "Yz9FQ3", "xJ9ugb", "uJpz4i", "tVNPvm", "pGsrXL", "UaiUNA", "pLGzbw", "p8wppL",
    "NAs0hv", "OirGaB", "qxzCqK", "57LrbR", "BCjtS3", "bKnfGi", "pYT7uA", "EXRaNP",
    "eMlUHa", "LEXGOe", "ijMbAY", "IOGvJR", "g3JoRU", "jNHLCw", "jZsRAq", "otMns8",
    "91DIUR", "3I0MGA", "vqKJEd", "GJHodm", "8RJtNN", "JBvFsy", "5Eek5u", "mXG53D",
    "RiqLdw", "M8ZKZX", "C9VOA9", "JzKcDQ", "YMUKJX", "Gagi79", "Yfk1YD", "oWNIfO",
    "1C0ah3", "eNhVk3", "BgywEW", "Su3dWV", "i0Epjd", "EB6Cri", "wIwXXe", "pxTW4F",
    "1uf3rX", "gJmJK9", "j20qGS", "3yAl4x", "hGY4zP"

]

async def simulate_clicks(code: str, num_clicks: int):
    async with httpx.AsyncClient() as client:
        for i in range(num_clicks):
            response = await client.get(f"{BASE_URL}/{code}", follow_redirects=False)
            if response.status_code in [302, 307]:
                print(f"✅ Clicked on /{code} [{i+1}/{num_clicks}]")
            else:
                print(f"❌ Error on /{code}: {response.status_code}")
            await asyncio.sleep(0.1)

async def main():
    tasks = []
    for code in CODES:
        num = random.randint(1, 10)
        tasks.append(simulate_clicks(code, num))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
