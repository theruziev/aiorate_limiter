from functools import partial

from starlette.applications import Starlette
from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn
from starlette.types import ASGIApp, Scope, Receive, Send, Message

from aiorate_limiter import RateLimiterResult
from aiorate_limiter.base import RateLimiterOpts
from aiorate_limiter.storage.memory import MemoryRateLimiter

app = Starlette(debug=True)

limiter = MemoryRateLimiter(RateLimiterOpts(points=2, duration=5000))


async def unattached_send(message: Message) -> None:
    raise RuntimeError("send awaitable not set")  # pragma: no cover


class RateLimiterMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.send = unattached_send
        self.rl_res = None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        self.send = send
        request = Request(scope, receive)
        res = await limiter.consume(request.client.host)
        self.rl_res = res
        if res.is_allowed:
            await self.app(scope, receive, self.send_wrapper)
            return

        response = JSONResponse({"error": "To many requests"}, status_code=429)
        await response(scope, receive, self.send_wrapper)

    async def send_wrapper(self, msg: Message):
        if msg["type"] == "http.response.start":
            result = self.rl_res
            headers = MutableHeaders(scope=msg)
            headers.append("X-Rate-Limit-Limit", str(result.consumed_points))
            headers.append("X-Rate-Limit-Remaining", str(result.remaining_points))
            headers.append("X-Rate-Limit-Reset", str(result.ms_before_next))
        await self.send(msg)


@app.route("/")
async def homepage(request):
    return JSONResponse({"hello": "world"})


if __name__ == "__main__":
    app.add_middleware(RateLimiterMiddleware)
    uvicorn.run(app, host="127.0.0.1", port=8000)
