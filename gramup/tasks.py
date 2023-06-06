from pathlib import Path

from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterDocument

from gramup.constants import API_ID, API_HASH
from gramup.models import File, Folder, Task


async def pull_all_to_db(task: Task):
    client = TelegramClient("anon", API_ID, API_HASH)

    await client.connect()

    if not await client.is_user_authorized():
        task.status = "failed"
        task.message = "User not authorized"
        task.save()
        return

    try:
        async for message in client.iter_messages("me", filter=InputMessagesFilterDocument):
            m_id = message.id
            caption: str = message.message
            path = Path(caption if "/" in caption else f"external/{caption}")

            file, created = File.get_or_create(
                id=m_id,
                path=str(path),
            )

            if not created:
                continue

            file.name = path.name
            file.save()

            for folder in path.parents:
                file_new, created = File.get_or_create(
                    path=str(folder),
                    is_folder=True
                )

                if not created:
                    break

                folder_new, _ = Folder.get_or_create(this=file_new)
                file_new.name = folder.name
                folder_new.files.add(file)
                folder_new.save()

                file = folder_new
    except Exception as e:
        task.status = "failed"
        task.message = f"Something went wrong: {e}"
        task.save()
        raise e

    task.status = "completed"
    task.save()
