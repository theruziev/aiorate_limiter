import aioredis
import pytest

from aiorate_limiter import RateLimiterOpts
from aiorate_limiter.storage.redis import RedisRateLimiter, REDIS_SCRIPT_HASH


@pytest.fixture
async def redis():
    redis = await aioredis.create_redis("redis://localhost:6379")

    yield redis

    redis.close()
    await redis.wait_closed()


@pytest.mark.asyncio
async def test_consume(redis):
    key, duration, points = "test_key", 5000, 10
    opts = RateLimiterOpts(points=points, duration=duration)
    redis_limiter = RedisRateLimiter(opts, redis)
    await redis_limiter.init()
    res = await redis_limiter.consume(key, 0)
    assert res.is_allowed and res.remaining_points == points
    # Reduce points
    res = await redis_limiter.consume(key)
    assert res.is_allowed and res.remaining_points == points - 1
    # Reduce token
    res = await redis_limiter.consume(key)
    assert res.is_allowed and res.remaining_points == points - 2
    # Reduce all tokens
    res = await redis_limiter.consume(key, points * 10)
    assert res.is_allowed is False


@pytest.mark.asyncio
async def test_script_load(redis):
    key, duration, points = "test_key", 5000, 5
    opts = RateLimiterOpts(points=points, duration=duration)
    redis_limiter = RedisRateLimiter(opts, redis)
    await redis_limiter.init()
    assert (await redis.script_exists(REDIS_SCRIPT_HASH))[0]
    # Check success loading script
    await redis_limiter.consume(key, 0)
    # Remove script
    await redis.script_flush()
    assert not (await redis.script_exists(REDIS_SCRIPT_HASH))[0]
    with pytest.raises(Exception):
        await redis_limiter.consume(key, 0)
