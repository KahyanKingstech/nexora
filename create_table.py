# from database import get_db_connection
# import asyncio

# async def create_tables():
#     conn = await get_db_connection()
#     async with conn.cursor() as cursor:
#         await cursor.execute("""
#             CREATE TABLE IF NOT EXISTS department (
#                 department_id VARCHAR(50) PRIMARY KEY,
#                 department_name VARCHAR(100) NOT NULL
#             )
#         """)
#         await conn.commit()
#     conn.close()


from database import get_db_connection
import asyncio

async def create_tables():
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        # Create Department Table
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS department (
                department_id VARCHAR(50) PRIMARY KEY,
                department_name VARCHAR(100) NOT NULL
            )
        """)

        # Create Employee Table
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                employee_id VARCHAR(50) PRIMARY KEY,
                employee_name VARCHAR(100) NOT NULL,
                gender VARCHAR(10) NOT NULL,
                email VARCHAR(50) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                department_id VARCHAR(50),
                FOREIGN KEY (department_id) REFERENCES department(department_id) ON DELETE SET NULL
            )
        """)

        await conn.commit()
    conn.close()

