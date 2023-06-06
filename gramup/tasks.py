from pathlib import Path

from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterDocument

from gramup.constants import API_ID, API_HASH, DB_PATH
from gramup.models import Task


async def pull_all_to_db(task: Task):
    client = TelegramClient("anon", API_ID, API_HASH)

    await client.connect()

    if not await client.is_user_authorized():
        task.status = "failed"
        task.message = "User not authorized"
        task.save()
        return

    try:
        to_write = {}
        async for message in client.iter_messages("me", filter=InputMessagesFilterDocument):
            m_id = str(message.id)
            caption: str = message.message
            path = Path(caption)
            name = path.name
            path = path if path.parent != "." else path.joinpath("external")
            path = str(Path(DB_PATH).joinpath("files", path).with_name("files.txt"))

            if path not in to_write:
                to_write[path] = []

            to_write[path].append(" ".join((m_id, name)))

        for path, messages in to_write.items():
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("\n".join(messages))

    except Exception as e:
        task.status = "failed"
        task.message += f"Something went wrong: {e}"
        task.save()
        raise e

    task.status = "completed"
    task.save()
