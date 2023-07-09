import asyncio
import glob
import os
from pathlib import Path
from typing import List

from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from telethon import TelegramClient

from constants import API_ID, API_HASH, DB_PATH
from gramup.models import Task
from gramup.tasks import pull_all_to_db, upload

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


@app.get("/api/auth/")
async def auth(action="check"):
    if not client.is_connected():
        await client.connect()

    if action == "check":
        return {"auth": await client.is_user_authorized()}

    if action == "logout":
        await client.log_out()

    return {"auth": False}


@app.get("/api/files/")
async def files(path=".") -> List:
    ret = []

    base = Path(DB_PATH).joinpath("files")
    path_obj = base.joinpath(path)

    if not path_obj.exists():
        return []

    for file in path_obj.iterdir():
        if file.is_dir():
            ret.append({
                "folder": True,
                "name": file.name,
                "path": str(file.relative_to(base)),
                "id": ""
            })

    for line in path_obj.joinpath("files.txt").read_text().split("\n"):
        file_id, file_name = line.split("~", 1)
        ret.append({
            "folder": False,
            "name": file_name,
            "path": str(path_obj.joinpath(file_name).relative_to(base)),
            "id": file_id
        })

    return ret


@app.get("/api/local_files/")
async def local_files(path="") -> List:
    return [
        {
            "folder": os.path.isdir(file),
            "name": os.path.basename(file),
            "path": file,
            "id": ""
        }
        for file in glob.glob(f"{path}/*")
    ]


@app.post("/api/tasks/")
async def tasks(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    if "source" not in body or "destination" not in body:
        raise HTTPException(status_code=400, detail="Source and destination are required")

    if "action" not in body:
        raise HTTPException(status_code=400, detail="Action is required")

    if body["action"] not in ["upload", "sync"]:
        raise HTTPException(status_code=400, detail="Unknown action")

    task = Task(f"{body['action'].title()} {body['source']}")
    task.save()

    functions = {
        "upload": upload,
        "sync": sync
    }

    background_tasks.add_task(
        functions[body["action"]],
        task,
        Path(body["source"]),
        Path(body["destination"])
    )

    return task.signature()


@app.get("/api/tasks/")
async def tasks_list():
    return [task.signature() for task in Task.list()]


@app.get("/api/pull_all/")
async def pull_all(background_tasks: BackgroundTasks):
    task = Task("Pull all files")
    task.save()
    background_tasks.add_task(pull_all_to_db, task=task)

    return task.id


app.mount("/", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
