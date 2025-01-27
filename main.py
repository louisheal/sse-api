import time

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


async def event_generator():
    while True:
        # This is where you would implement your real-time data generation
        yield f"data: {time.time()}\n\n"
        time.sleep(1)  # simulate some delay in sending data


@app.get("/events")
async def sse():
    return StreamingResponse(event_generator())


if __name__ == "__main__":
    uvicorn.run(app)
