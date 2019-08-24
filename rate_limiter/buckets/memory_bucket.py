import asyncio
from typing import Tuple

from rate_limiter.base import BaseTokenBucket


class MemoryTokenBucket(BaseTokenBucket):
    def __init__(self, refill_time: int, max_amount: int):
        self.max_amount = max_amount
        self.refill_time = refill_time
        self.data = {}
        self.lock = asyncio.Lock()

    async def reduce(self, key: str, tokens: int) -> Tuple[bool, int]:
        async with self.lock:
            build_key = self._build_key(key)
            tokens_key, timestamp_key = f"{build_key}.tokens", f"{build_key}.ts"

            value = self.data.get(tokens_key, self.max_amount)
            last_update = self.data.get(timestamp_key, self._get_time())

            refill_count = int((self._get_time() - last_update) / self.refill_time)

            value += refill_count * self.max_amount
            last_update += refill_count * self.refill_time

            if value >= self.max_amount:
                value, last_update = self.max_amount, self._get_time()

            allowed = value >= tokens
            value = value - tokens if allowed else value

            self.data[tokens_key] = value
            self.data[timestamp_key] = last_update
            return allowed, value

    def _build_key(self, key: str) -> str:
        return key
