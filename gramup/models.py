import json
from datetime import datetime
from pathlib import Path

import shortuuid

from gramup.constants import DB_PATH


class Task:
    def __init__(self, name=None, db_path=DB_PATH):
        self.id = shortuuid.uuid()
        self.status = "running"
        self.message = ""
        self.__name = name
        self.__schedule_time = datetime.now()

        self.db_file = Path(db_path).joinpath(self.__class__.__name__, f"{self.id}")

    def __repr__(self):
        return f"<Task {self.__name} {self.status}>"

    def __str__(self):
        return self.__repr__()

    def signature(self):
        return {
            "id": self.id,
            "name": self.__name,
            "status": self.status,
            "schedule_time": self.__schedule_time.isoformat()
        }

    def to_dict(self):
        return {
            **self.signature(),
            "message": self.message,
        }

    def set(self, *, status=None, message=None):
        self.status = status or self.status
        if message is not None:
            self.message += message

        self.save()

    def load(self, task_id, db_path=DB_PATH):
        self.id = task_id
        self.db_file = Path(db_path).joinpath(Task.__name__, self.id)

        if not self.db_file.exists():
            raise FileNotFoundError(f"Task {self.id} not found")

        data = json.loads(self.db_file.read_text())

        self.status = data["status"]
        self.message = data["message"]
        self.__name = data["name"]
        self.__schedule_time = datetime.fromisoformat(data["schedule_time"])

        return self

    def save(self):
        if not self.db_file.parent.exists():
            self.db_file.parent.mkdir(parents=True)

        self.db_file.write_text(json.dumps(self.to_dict()))

    @staticmethod
    def list(db_path=DB_PATH):
        db_path = Path(db_path).joinpath(Task.__name__)

        if not db_path.exists():
            db_path.mkdir()

        return [Task().load(task_id.name) for task_id in db_path.iterdir()]
