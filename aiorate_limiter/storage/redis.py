import hashlib
import time
from aioredis import Redis
from ..base import RateLimiterAbstract, RateLimiterResult, RateLimiterOpts

REDIS_TOKEN_BUCKET_SCRIPT = """
local tokens_key = KEYS[1]
local timestamp_key = KEYS[2]
local duration = tonumber(ARGV[1])
local max_points = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local points = tonumber(ARGV[4])
local data = redis.call("mget", tokens_key, timestamp_key)

local value = tonumber(data[1])
local last_update = tonumber(data[2])
if value == nil then
    value = max_points
end
if last_update == nil then
    last_update = now
end

local refill_count = (now - last_update) / duration 

value = value + (refill_count * max_points)
last_update = last_update + (refill_count * duration)

if value >= max_points then
    value = max_points
    last_update = now
end

local available_points =math.floor(value - points)
if value >= points then
    value = available_points
end
local ttl = math.floor((last_update * 2) / 1000)
redis.call("setex", tokens_key, ttl, value)
redis.call("setex", timestamp_key, ttl, last_update)

return { available_points, last_update }
"""  # noqa

REDIS_SCRIPT_HASH = hashlib.sha1(REDIS_TOKEN_BUCKET_SCRIPT.encode()).hexdigest()  # noqa


class RedisRateLimiter(RateLimiterAbstract):
    def __init__(self, opts: RateLimiterOpts, redis: Redis):
        self.opts = opts
        self.redis = redis

    async def init(self):
        await self._load_script()

    async def _load_script(self):
        """
        Load lua token-bucket implementation
        """
        script_exist = bool((await self.redis.script_exists(REDIS_SCRIPT_HASH))[0])
        if not script_exist:
            await self.redis.script_load(REDIS_TOKEN_BUCKET_SCRIPT)

    async def consume(self, key: str, points: int = 1) -> RateLimiterResult:
        build_key = self._build_key(key)
        keys = [f"{build_key}:tokens", f"{build_key}:ts"]
        value, last_update = await self.redis.evalsha(
            REDIS_SCRIPT_HASH,
            keys=keys,
            args=[self.opts.duration, self.opts.points, self._get_time(), points],
        )
        return RateLimiterResult(
            remaining_points=value,
            ms_before_next=self._get_time() - last_update,
            consumed_points=points,
        )

    @classmethod
    def _get_time(cls) -> int:
        """
        returning milliseconds of timestamp
        :return:
        """
        return int(time.time() * 1000)

    def _build_key(self, key: str) -> str:
        return f"{self.opts.key_prefix}:{key}"
