import hashlib

import aioredis
import pytest

from rate_limiter.buckets.redis_bucket import RedisTokenBucket, REDIS_SCRIPT_HASH


@pytest.fixture
async def redis():
    redis = await aioredis.create_redis("redis://localhost:6379")
    yield redis

    redis.close()
    await redis.wait_closed()


@pytest.mark.asyncio
async def test_reduce(redis):
    key, refill_time, max_amount = "test_key", 5, 10
    tb = RedisTokenBucket(redis=redis, refill_time=refill_time, max_amount=max_amount)
    await tb.init()
    allowed, available_tokens = await tb.reduce(key, 0)
    assert allowed and available_tokens == tb.max_amount
    # Reduce token
    allowed, available_tokens = await tb.reduce(key, 1)
    assert allowed and available_tokens == tb.max_amount - 1
    # Reduce token
    allowed, available_tokens = await tb.reduce(key, 1)
    assert allowed and available_tokens == max_amount - 2
    # Reduce all tokens
    allowed, available_tokens = await tb.reduce(key, max_amount * 10)
    assert allowed is False


@pytest.mark.asyncio
async def test_script_load(redis):
    key, refill_time, max_amount = "test_key", 5, 10
    tb = RedisTokenBucket(redis=redis, refill_time=refill_time, max_amount=max_amount)
    await tb.init()
    assert (await redis.script_exists(REDIS_SCRIPT_HASH))[0]
    # Check success loading script
    await tb.reduce(key, 0)
    # Remove script
    await redis.script_flush()
    assert not (await redis.script_exists(REDIS_SCRIPT_HASH))[0]
    with pytest.raises(Exception):
        await tb.reduce(key, 0)
