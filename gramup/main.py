import asyncio
import glob
import os
from typing import List, Literal

from fastapi import FastAPI, HTTPException, Request
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from telethon import TelegramClient

from constants import API_ID, API_HASH
from gramup.models import File, Task, TaskRequest

client = TelegramClient('anon', API_ID, API_HASH)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.websocket("/api/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    if not client.is_connected():
        await client.connect()

    if await client.is_user_authorized():
        return await websocket.send_json({"type": "connection", "status": "connected"})

    qr = await client.qr_login()
    await websocket.send_json({"url": qr.url, "type": "qr"})

    while True:
        try:
            if await qr.wait(10):
                break
        except asyncio.exceptions.TimeoutError:
            await qr.recreate()
            await websocket.send_json({"url": qr.url, "type": "qr"})

    await websocket.send_json({"type": "connection", "status": "connected"})

    await websocket.close()


@app.get("/api/files/")
async def files(path="") -> List[File]:
    if not client.is_connected() or not await client.is_user_authorized():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    return []


@app.get("/api/local_files/")
async def local_files(path="") -> List[File]:
    return [
        File(
            folder=os.path.isdir(file),
            name=os.path.basename(file),
            path=file,
            id=""
        )
        for file in glob.glob(f"{path}/*")
    ]


@app.post("/api/tasks/")
async def tasks(request: Request) -> Task:
    body = TaskRequest(**(await request.json()))

    return Task(
        id="",
        name="",
        status="running",
    )


app.mount("/", StaticFiles(directory="static"), name="static")
