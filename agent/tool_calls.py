import aiomysql
import asyncio

async def fetch_from_db(query):
    try:
        conn = await aiomysql.connect(
        host="localhost",
        user="root",
        password="",
        db="fd_data"
        )
        async with conn.cursor() as cursor:
            await cursor.execute(query)
            result = await cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        return f"Error accessing database: {str(e)}"
