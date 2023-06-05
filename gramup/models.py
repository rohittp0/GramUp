from typing import Literal, TypedDict

from pydantic import BaseModel


class File(BaseModel):
    folder: bool
    name: str
    path: str
    id: str


class Task(BaseModel):
    id: str
    name: str
    status: Literal["running", "stopped", "finished"]


TaskRequest = TypedDict("TaskRequest", {"path": str, "type": Literal["sync", "upload"]})
