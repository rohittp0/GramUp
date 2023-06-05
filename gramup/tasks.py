from pathlib import Path

from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterDocument

from gramup.models import File, Folder, Task


async def pull_all_to_db(task: Task):
    client = TelegramClient("session", 1234, "asdf")

    if not client.is_connected():
        await client.connect()

    if not await client.is_user_authorized():
        task.status = "failed"
        task.save()
        return

    for message in client.iter_messages("me", filter=InputMessagesFilterDocument):
        m_id = message.id
        caption: str = message.caption
        path = Path(caption if "/" in caption else f"external/{caption}")

        file = File.create(
            id=m_id,
            path=str(path),
            name=path.name
        )

        file.save()
        first = True

        for folder in path.parents:
            folder_new, _ = Folder.get_or_create(
                path=str(folder),
                name=folder.name
            )

            if first:
                first = False
                folder_new.files.add(file)
            else:
                folder_new.sub_folders.add(file)

            folder_new.save()
            file = folder_new

    task.status = "completed"
    task.save()
