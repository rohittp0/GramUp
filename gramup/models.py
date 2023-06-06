from datetime import datetime
from typing import Literal, TypedDict

import peewee
import shortuuid

db = peewee.SqliteDatabase('database.db')
db.autoconnect = True


class BaseModel(peewee.Model):
    id = peewee.CharField(primary_key=True, max_length=22, default=lambda: shortuuid.uuid())

    class Meta:
        database = db


class File(BaseModel):
    name = peewee.CharField(max_length=128, default=".")
    path = peewee.CharField(max_length=512, unique=True)
    is_folder = peewee.BooleanField(default=False)


class Folder(BaseModel):
    this = peewee.ForeignKeyField(File, backref="this_folder", on_delete="CASCADE")
    files = peewee.ManyToManyField(File, backref="folder", on_delete="CASCADE")


class Task(BaseModel):
    name = peewee.CharField(max_length=128)
    status = peewee.CharField(choices=["running", "completed", "failed"], default="running")
    schedule_time = peewee.DateTimeField(default=datetime.now)
    message = peewee.CharField(max_length=256, null=True)


FolderFile = Folder.files.get_through_model()

db.connect()
db.create_tables([File, FolderFile, Folder, Task])

TaskRequest = TypedDict("TaskRequest", {"path": str, "type": Literal["sync", "upload"]})
