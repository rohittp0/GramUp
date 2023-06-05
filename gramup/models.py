from datetime import datetime
from typing import Literal, TypedDict

import peewee
import shortuuid

db = peewee.SqliteDatabase('database.db')
db.autoconnect = True


class BaseModel(peewee.Model):
    id = peewee.CharField(primary_key=True,max_length=128, default=lambda: shortuuid.uuid(pad_length=128))

    class Meta:
        database = db


class File(BaseModel):
    name = peewee.CharField(max_length=128)
    path = peewee.CharField(max_length=128)
    folder = peewee.BooleanField(default=False)


class Folder(BaseModel):
    this = peewee.ForeignKeyField(File, backref="this_folder", on_delete="CASCADE")
    sub_folders = peewee.ManyToManyField(File, backref="parent_folder", on_delete="CASCADE")
    files = peewee.ManyToManyField(File, backref="folder", on_delete="CASCADE")


class Task(BaseModel):
    name = peewee.CharField(max_length=128)
    status = peewee.CharField(choices=["running", "completed", "failed"], default="running")
    schedule_time = peewee.DateTimeField(default=datetime.now)


FolderSubFolder = Folder.sub_folders.get_through_model()
FolderFile = Folder.files.get_through_model()

db.create_tables([File, FolderSubFolder, FolderFile, Folder, Task])

TaskRequest = TypedDict("TaskRequest", {"path": str, "type": Literal["sync", "upload"]})
