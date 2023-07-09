import asyncio
from pathlib import Path

from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterDocument

from gramup.constants import API_ID, API_HASH, DB_PATH
from gramup.models import Task


async def get_client(task):
    client = TelegramClient("anon", API_ID, API_HASH)

    await client.connect()

    if not await client.is_user_authorized():
        task.set(status="failed", message="Not authorized")
        return

    return client


async def pull_all_to_db(task: Task):
    client = await get_client(task)

    if not client:
        return

    try:
        to_write = {}
        async for message in client.iter_messages("me", filter=InputMessagesFilterDocument):
            m_id = str(message.id)
            caption: str = message.message
            path = Path(caption)
            name = path.name
            path = str(Path(DB_PATH).joinpath("files", path).with_name("files.txt"))

            if path not in to_write:
                to_write[path] = []

            to_write[path].append(f"{m_id}~{name}")

        for path, messages in to_write.items():
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("\n".join(messages), encoding='utf-8')

    except Exception as e:
        task.set(status="failed", message=f"Something went wrong: {e}")

    task.set(status="completed")


async def upload(task: Task, source: Path, destination: Path, branch=False):
    client = await get_client(task)

    if not client:
        return

    try:
        sources = []

        if source.is_dir():
            tasks = []
            for file in source.iterdir():
                if file.is_file():
                    sources.append(file)
                else:
                    tasks.append(upload(task, file, destination.joinpath(file.name), branch=True))

            status = await asyncio.gather(*tasks, return_exceptions=True)
            if any(status):
                task.set(status="failed", message=f"Something went wrong: {status}")

        else:
            sources = [source]

        tasks = []

        for source in sources:
            caption = str(destination.joinpath(source.name))
            tasks.append(client.send_file("me", str(source), caption=caption, force_document=True))

        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        task.set(status="failed", message=f"Something went wrong: {e}")
        return

    if not branch:
        task.set(status="completed")
    else:
        task.set(message=f"Uploaded {source.name}")
