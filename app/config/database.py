from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

async def connect_to_mongo():
    try:
        # Attempt to fetch server information to check connection
        await client.server_info()
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e 