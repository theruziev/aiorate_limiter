import aioredis

from aiorate_limiter.base import RateLimiterOpts
from aiorate_limiter.storage.memory import MemoryRateLimiter
from aiorate_limiter.storage.redis import RedisRateLimiter
import asyncio


async def memory_rate_limit_example():
    # Limit to 5 query for every 5 second
    opts = RateLimiterOpts(points=5, duration=5000)
    limiter = MemoryRateLimiter(opts)
    await limiter.init()
    for i in range(10):
        res = await limiter.consume("user1")
        print(f"Allow:{res.is_allowed}, Available tokens: {res.remaining_points}")
    print("sleep for 5 second")
    await asyncio.sleep(5)
    for i in range(10):
        res = await limiter.consume("user1")
        print(f"Allow:{res.is_allowed}, Available tokens: {res.remaining_points}")


async def redis_rate_limit_example():
    # Limit to 5 query for every 5 second
    redis = await aioredis.create_redis("redis://localhost:6379")
    opts = RateLimiterOpts(points=5, duration=5000)
    redis_limiter = RedisRateLimiter(opts, redis)
    await redis_limiter.init()
    for i in range(10):
        res = await redis_limiter.consume("user1")
        print(f"Allow:{res.is_allowed}, Available tokens: {res.remaining_points}")
    print("sleep for 5 second")
    await asyncio.sleep(5)
    for i in range(10):
        res = await redis_limiter.consume("user1")
        print(f"Allow:{res.is_allowed}, Available tokens: {res.remaining_points}")
