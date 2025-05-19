import aiohttp
import asyncio
import json
from datetime import date

async def download_data():
    await asyncio.sleep(2)
    url = "https://www.federalregister.gov/api/v1/documents.json"
    params = {
        "per_page": 5,
        "order": "newest",
        "conditions[publication_date][gte]": str(date.today())
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            with open("raw_data.json", "w") as f:
                json.dump(data, f)
            print("Data downloaded successfully.")

# asyncio.run(download_data())
