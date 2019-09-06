from aiohttp import web

from aiorate_limiter.base import RateLimiterOpts
from aiorate_limiter.storage.memory import MemoryRateLimiter

limiter = MemoryRateLimiter(RateLimiterOpts(points=2, duration=5000))


async def hello(request):
    return web.Response(text=str(request["points"]))


@web.middleware
async def limiter_middleware(request, handler):
    res = await limiter.consume(request.remote)
    if res.is_allowed:
        request["points"] = res.remaining_points
        response = await handler(request)
    else:
        response = web.Response(text="To many requests", status=429)

    response.headers["X-Rate-Limit-Limit"] = str(res.consumed_points)
    response.headers["X-Rate-Limit-Remaining"] = str(res.remaining_points)
    response.headers["X-Rate-Limit-Reset"] = str(res.ms_before_next)

    return response


if __name__ == "__main__":
    app = web.Application(middlewares=[limiter_middleware])
    app.add_routes([web.get("/", hello)])
    web.run_app(app, host="127.0.0.1")
