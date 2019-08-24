import hashlib
from typing import Tuple

from aioredis import Redis

from rate_limiter.base import BaseTokenBucket

REDIS_TOKEN_BUCKET_SCRIPT = """
local tokens_key = KEYS[1]
local timestamp_key = KEYS[2]
local refill_time = tonumber(ARGV[1])
local max_amount = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local tokens = tonumber(ARGV[4])
local data = redis.call("mget", tokens_key, timestamp_key)

local value = tonumber(data[1])
local last_update = tonumber(data[2])
if value == nil then
    value = max_amount
end
if last_update == nil then
    last_update = now
end

local refill_count = (now - last_update) / refill_time 

value = value + (refill_count * max_amount)
last_update = last_update + (refill_count * refill_time)

if value >= max_amount then
    value = max_amount
    last_update = now
end

local allowed = value >= tokens
if allowed then
    value = value - tokens
end
local ttl = last_update * 2
redis.call("setex", tokens_key, ttl, value)
redis.call("setex", timestamp_key, ttl, last_update)

return { allowed, value }
"""  # noqa

REDIS_SCRIPT_HASH = hashlib.sha1(REDIS_TOKEN_BUCKET_SCRIPT.encode()).hexdigest()  # noqa


class RedisTokenBucket(BaseTokenBucket):
    def __init__(self, redis: Redis, refill_time: int, max_amount: int, prefix: str = ""):
        """

        :param redis: Redis Connection
        :param refill_time:
        :param max_amount:
        :param prefix:
        """
        self.redis = redis
        self.max_amount = max_amount
        self.refill_time = refill_time
        self.prefix = prefix

    async def init(self):
        """
        Async constructor
        :return:
        """
        await self._load_script()

    async def _load_script(self):
        """
        Load token-bucket implementation lua script
        :return:
        """
        script_exist = bool((await self.redis.script_exists(REDIS_SCRIPT_HASH))[0])
        if not script_exist:
            await self.redis.script_load(REDIS_TOKEN_BUCKET_SCRIPT)

    async def reduce(self, key: str, tokens: int) -> Tuple[bool, int]:
        build_key = self._build_key(key)
        keys = [f"{build_key}:tokens", f"{build_key}:ts"]
        allowed, available_token = await self.redis.evalsha(
            REDIS_SCRIPT_HASH,
            keys=keys,
            args=[self.refill_time, self.max_amount, self._get_time(), tokens],
        )
        return bool(allowed), available_token

    def _build_key(self, key: str) -> str:
        return f"{self.prefix}:{key}"
