import asyncio
import time
from typing import Dict

from ..base import RateLimiterAbstract, RateLimiterOpts, RateLimiterResult


class MemoryRateLimiter(RateLimiterAbstract):
    def __init__(self, opts: RateLimiterOpts):
        self.opts = opts
        self.data: Dict[str, int] = {}
        self.lock = asyncio.Lock()

    async def init(self):
        pass

    async def consume(self, key: str, points: int = 1) -> RateLimiterResult:
        async with self.lock:
            build_key = self._build_key(key)
            tokens_key, timestamp_key = f"{build_key}.tokens", f"{build_key}.ts"

            value = self.data.get(tokens_key, self.opts.points)
            last_update = self.data.get(timestamp_key, self._get_time())

            refill_count = int((self._get_time() - last_update) / self.opts.duration)
            value += refill_count * self.opts.points
            last_update += refill_count * self.opts.duration

            if value >= self.opts.points:
                value, last_update = self.opts.points, self._get_time()
            available_points = value - points
            value = available_points if value >= points else value
            self.data[tokens_key] = value
            self.data[timestamp_key] = last_update
            return RateLimiterResult(
                remaining_points=available_points,
                ms_before_next=self._get_time() - last_update,
                consumed_points=points,
            )

    @classmethod
    def _get_time(cls) -> int:
        """
        Return monotonic milliseconds
        """
        return int(time.monotonic() * 1000)

    def _build_key(self, key: str) -> str:
        return f"{self.opts.key_prefix or ''}_{key}"
