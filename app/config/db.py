from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

client = AsyncIOMotorClient(settings.database_client)
db = client[settings.database_name]


async def get_db() -> AsyncIOMotorClient:
    return db


async def connect_to_db():
    """Connect to the database and test the connection."""

    try:

        # Test the connection with a ping command
        await db.command("ping")
        print("Database connection successful")
        return db

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise e


async def close_db_connection():
    global client
    if client:
        client.close()
        print("Database connection closed")
