from database import get_db_connection
import asyncio

async def create_tables():
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS department (
                department_id VARCHAR(50) PRIMARY KEY,
                department_name VARCHAR(100) NOT NULL
            )
        """)
        await conn.commit()
    conn.close()
