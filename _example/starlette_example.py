from starlette.applications import Starlette
from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn
from starlette.types import ASGIApp, Scope, Receive, Send, Message

from aiorate_limiter.base import RateLimiterOpts
from aiorate_limiter.storage.memory import MemoryRateLimiter

app = Starlette(debug=True)

mem_rt = MemoryRateLimiter(RateLimiterOpts(points=2, duration=5000))


class RateLimiterMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)

        res = await mem_rt.consume(request.client.host)

        async def send_wrapper(msg: Message):
            if msg["type"] == "http.response.start":
                headers = MutableHeaders(scope=msg)
                headers.append("X-Rate-Limit-Limit", str(res.consumed_points))
                headers.append("X-Rate-Limit-Remaining", str(res.remaining_points))
                headers.append("X-Rate-Limit-Reset", str(res.ms_before_next))
            await send(msg)

        if res.is_allowed:
            await self.app(scope, receive, send_wrapper)
            return
        response = JSONResponse({"error": "To many requests"}, status_code=429)
        await response(scope, receive, send_wrapper)


@app.route("/")
async def homepage(request):
    return JSONResponse({"hello": "world"})


if __name__ == "__main__":
    app.add_middleware(RateLimiterMiddleware)
    uvicorn.run(app, host="127.0.0.1", port=8000)
