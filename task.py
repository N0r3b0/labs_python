from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Task:
    id: int
    name: str
    description: str = ""
    status: str = "Started"
    created_at: datetime = field(default_factory=datetime.today)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d") if self.created_at else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            status=data.get("status", "Started"),
            created_at=datetime.strptime(data["created_at"], "%Y-%m-%d") if data.get("created_at") else None
        )


class TaskManager:
    tasks: Dict[int, Task] = {}
    id_counter: int = 0

    @classmethod
    def add_task(cls, task: Task) -> None:
        cls.tasks[task.id] = task

    @classmethod
    def remove_task(cls, task_id: int) -> None:
        cls.tasks.pop(task_id, None)

    @classmethod
    def get_task(cls, task_id: int) -> Task:
        return cls.tasks.get(task_id)

    @classmethod
    def clear_all(cls) -> None:
        cls.tasks.clear()