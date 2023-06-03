import asyncio

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket
from telethon import TelegramClient

from constants import API_ID, API_HASH

client = TelegramClient('anon', API_ID, API_HASH)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

icons_path = "static/icons"

templates = Jinja2Templates(directory="templates")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

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


@app.get("/sw.js")
def get_sw():
    return FileResponse("static/js/sw.js", media_type="text/javascript")


@app.get("/manifest.json")
def get_manifest():
    return FileResponse("static/manifest.json", media_type="application/json")


@app.get("/login")
async def login(request: Request):
    if not client.is_connected():
        await client.connect()

    if await client.is_user_authorized():
        return RedirectResponse(url="/", status_code=302)

    context = {"request": request}

    return templates.TemplateResponse("login.html", context=context)


@app.get("/{folder:path}")
async def files(request: Request, folder="", error=""):
    if not client.is_connected() or not await client.is_user_authorized():
        return RedirectResponse(url="/login", status_code=302)

    context = {}

    return templates.TemplateResponse("files.html", context=context)
