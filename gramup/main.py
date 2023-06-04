import asyncio

from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from telethon import TelegramClient

from constants import API_ID, API_HASH

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
async def files(path=""):
    if not client.is_connected() or not await client.is_user_authorized():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    return []


app.mount("/", StaticFiles(directory="static"), name="static")
