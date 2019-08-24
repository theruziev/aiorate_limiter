import time
from abc import ABC, abstractmethod
from typing import Tuple


class BaseTokenBucket(ABC):
    async def init(self):
        pass  # pragma: no cover

    @classmethod
    def _get_time(cls):
        return int(time.time())  # pragma: no cover

    @abstractmethod
    async def reduce(self, key: str, tokens: int) -> Tuple[bool, int]:
        pass  # pragma: no cover

    @abstractmethod
    async def _build_key(self, key: str) -> str:
        pass  # pragma: no cover
