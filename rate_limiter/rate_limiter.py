from typing import Tuple

from rate_limiter.base import BaseTokenBucket


class RateLimiter:
    def __init__(self, bucket: BaseTokenBucket):
        self.bucket = bucket

    async def allow(self, key: str, tokens: int = 1) -> Tuple[bool, int]:
        """

        :param key: str
        :param tokens: int
        :return: Allowed and available token
        """
        return await self.bucket.reduce(key, tokens)
