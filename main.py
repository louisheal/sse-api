import time

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


async def event_generator():
    while True:
        yield f"data: {time.time()}\n\n"
        time.sleep(1)


@app.get("/events")
async def sse():
    return StreamingResponse(event_generator())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
