import asyncio
import motor.motor_asyncio

async def test_conn():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
        res = await client.admin.command("ping")
        print("MONGO PING SUCCESS:", res)
    except Exception as e:
        print("MONGO PING FAILED:", e)

if __name__ == "__main__":
    asyncio.run(test_conn())
