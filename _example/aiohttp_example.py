from aiohttp import web
from aiohttp.web_exceptions import HTTPTooManyRequests

from aiorate_limiter.base import RateLimiterOpts
from aiorate_limiter.storage.memory import MemoryRateLimiter

opts = RateLimiterOpts(points=5, duration=5000)
limiter = MemoryRateLimiter(opts)


async def hello(request):
    return web.Response(text=str(request["points"]))


@web.middleware
async def limiter_middleware(request, handler):
    res = await limiter.consume(request.remote)
    if res.is_allowed:
        request["points"] = res.remaining_points
        return await handler(request)
    raise HTTPTooManyRequests()


if __name__ == "__main__":
    app = web.Application(middlewares=[limiter_middleware])
    app.add_routes([web.get("/", hello)])
    web.run_app(app, host="127.0.0.1")
