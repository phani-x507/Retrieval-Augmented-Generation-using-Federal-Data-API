import json
import aiomysql
import asyncio

async def update_database():
    with open("processed_data.json", "r") as f:
        records = json.load(f)

    conn = await aiomysql.connect(
        host="localhost",
        user="root",
        password="",
        db="fd_data"
    )
    async with conn.cursor() as cursor:
        for record in records:
            await cursor.execute("""
                INSERT INTO federal_register (title, summary, publication_date, agency)
                VALUES (%s, %s, %s, %s)
            """, (record['title'], record['summary'], record['publication_date'], record['agency']))
        await conn.commit()
    conn.close()
    print("Database updated successfully.")

asyncio.run(update_database())
