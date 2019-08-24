import pytest

from rate_limiter.buckets.memory_bucket import MemoryTokenBucket


@pytest.mark.asyncio
async def test_reduce():
    key, rate, capacity = "test_key", 5, 10
    tb = MemoryTokenBucket(refill_time=rate, max_amount=capacity)
    await tb.init()
    allowed, available_tokens = await tb.reduce(key, 0)
    assert allowed and available_tokens == tb.max_amount
    # Reduce token
    allowed, available_tokens = await tb.reduce(key, 1)
    assert allowed and available_tokens == tb.max_amount - 1
    # Reduce token
    allowed, available_tokens = await tb.reduce(key, 1)
    assert allowed and available_tokens == capacity - 2
    # Reduce all tokens
    allowed, available_tokens = await tb.reduce(key, capacity * 10)
    assert allowed is False
