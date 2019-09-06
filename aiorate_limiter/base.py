from abc import ABC, abstractmethod


class RateLimiterResult:
    __slots__ = ["remaining_points", "ms_before_next", "consumed_points"]

    def __init__(self, remaining_points: int, ms_before_next: int, consumed_points: int):
        """
        Result for consume limiter
        :param remaining_points: Number of remaining points in current duration
        :param ms_before_next: Number of milliseconds before next action can be done
        :param consumed_points: Number of consumed points in current duration
        """
        self.remaining_points = remaining_points
        self.ms_before_next = ms_before_next
        self.consumed_points = consumed_points

    @property
    def is_allowed(self) -> bool:
        """
        Result of consume, true if allow otherwise false
        """
        return self.remaining_points >= 0

    def __repr__(self):
        classname = self.__class__.__name__  # pragma: no cover
        return (
            f"{classname}(remaining_points={self.remaining_points}, "
            f"ms_before_next={self.ms_before_next}, consumed_points={self.consumed_points}, "
            f"is_allowed={self.is_allowed})"
        )  # pragma: no cover


class RateLimiterOpts:
    def __init__(self, points: int, duration: int, key_prefix: str = "rl"):
        """
        Common options for all implementation of RateLimiterAbstract

        :param points: Maximum number of points can be consumed over duration
        :param duration: Number of seconds before consumed points are reset
        :param key_prefix: for a specification prefix for key in a storage
        """
        self.points = points
        self.duration = duration
        self.key_prefix = key_prefix


class RateLimiterAbstract(ABC):
    """
    Interface for a RateLimiter
    """

    @abstractmethod
    async def init(self):
        """
        Async based constructor
        :return:
        """
        pass

    @abstractmethod
    async def consume(self, key: str, points: int = 1) -> RateLimiterResult:
        pass

    @abstractmethod
    async def factory(self, opts: RateLimiterOpts):
        pass
