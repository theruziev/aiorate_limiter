import pytest
from asynctest.mock import Mock

from rate_limiter.base import BaseTokenBucket
from rate_limiter.rate_limiter import RateLimiter


@pytest.mark.asyncio
@pytest.mark.parametrize("allowed, tokens", [(True, 1), (True, 50), (False, 0)])
async def test_rate_limiter(allowed, tokens):
    bucket_mock = Mock(BaseTokenBucket)
    bucket_mock.reduce.return_value = allowed, tokens

    rate_limiter = RateLimiter(bucket_mock)
    a, tok = await rate_limiter.allow("test_key")
    assert a == allowed
    assert tok == tokens
