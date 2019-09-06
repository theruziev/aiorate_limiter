import pytest

from aiorate_limiter import RateLimiterOpts
from aiorate_limiter.storage.memory import MemoryRateLimiter


@pytest.mark.asyncio
async def test_consume():
    key, duration, points = "test_key", 5000, 5
    opts = RateLimiterOpts(points=points, duration=duration)
    mem_limiter = MemoryRateLimiter(opts)
    await mem_limiter.init()
    res = await mem_limiter.consume(key, 0)
    assert res.is_allowed and res.remaining_points == points
    # Reduce points
    res = await mem_limiter.consume(key, 1)
    assert res.is_allowed and res.remaining_points == points - 1
    # Reduce token
    res = await mem_limiter.consume(key, 1)
    assert res.is_allowed and res.remaining_points == points - 2
    # Reduce all tokens
    res = await mem_limiter.consume(key, points * 10)
    assert res.is_allowed is False
