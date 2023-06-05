import asyncio
import glob
import os
from typing import List

import shortuuid
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from telethon import TelegramClient

from constants import API_ID, API_HASH
from gramup.models import File, Task, TaskRequest
from gramup.tasks import pull_all_to_db

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
async def files(path="") -> List:
    if not client.is_connected() or not await client.is_user_authorized():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    return []


@app.get("/api/local_files/")
async def local_files(path="") -> List:
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
async def tasks(request: Request, background_tasks: BackgroundTasks):
    body = TaskRequest(**(await request.json()))

    # background_tasks.add_task(

    return Task(
        id="",
        name="",
        status="running",
    )


@app.get("/api/tasks/")
async def tasks_list():
    ret = []

    for task in Task.select().order_by(Task.schedule_time.desc()):
        ret.append({
            "id": task.id,
            "name": task.name,
            "status": task.status,
            "schedule_time": task.schedule_time
        })

    return ret


@app.get("/api/pull_all/")
async def pull_all(background_tasks: BackgroundTasks):
    task, _ = Task.get_or_create(status="running", name="Pull all files")
    task.save()
    background_tasks.add_task(pull_all_to_db, task=task)

    return task.id


app.mount("/", StaticFiles(directory="static"), name="static")
