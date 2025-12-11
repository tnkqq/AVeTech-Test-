import redis.asyncio as aioredis  
from fastapi import HTTPException
from config import settings

client = aioredis.Redis(host=settings.RedisHost, port=settings.RedisPort, db=0)

async def get_redis() -> aioredis.Redis:
    try: 
        await client.ping()
    except:
        raise HTTPException(status_code=503, detail="Redis not connected")

    return client

