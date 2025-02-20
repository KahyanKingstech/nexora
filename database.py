import aiomysql

DB_CONFIG = {
    "host": "localhost",
    "user": "test_user",
    "password": "test_password",
    "db": "test_db",
    "autocommit": True  # Ensures queries execute immediately
}

async def get_db_connection():
    try:
        conn = await aiomysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None  # Return None if the connection fails
