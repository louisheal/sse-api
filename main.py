import asyncio
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from sse_starlette.sse import EventSourceResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response


queue = asyncio.Queue()


async def hello() -> ...:
    
    while True:
        data = await queue.get()
        yield {"data": data}


async def sse(request: Request) -> EventSourceResponse:
    return EventSourceResponse(hello())

async def random(request: Request) -> Response:
    data = await request.json()
    await queue.put(data)
    return Response("Success", 200)


middleware = [Middleware(CORSMiddleware, allow_origins=['*'])]
routes = [Route("/events", endpoint=sse), Route("/data", endpoint=random, methods=["POST"])]
app = Starlette(debug=True, routes=routes, middleware=middleware)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
