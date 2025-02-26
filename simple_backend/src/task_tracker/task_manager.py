import json
import os
from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    id: int
    title: str
    status: str

class TaskManager:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = self._load_tasks()
        self.next_id = max([task.id for task in self.tasks], default=0) + 1

    def _load_tasks(self) -> List[Task]:
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    return [Task(**task) for task in data]
            return []
        except json.JSONDecodeError:
            print(f"Error decoding {self.filename}, starting with empty list")
            return []
        except Exception as e:
            print(f"Unexpected error loading tasks: {e}")
            return []

    def _save_tasks(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump([task.dict() for task in self.tasks], f)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def get_all(self) -> List[Task]:
        return self.tasks

    def create(self, title: str, status: str = "todo") -> Task:
        task = Task(id=self.next_id, title=title, status=status)
        self.tasks.append(task)
        self.next_id += 1
        self._save_tasks()
        return task

    def update(self, task_id: int, title: Optional[str] = None, status: Optional[str] = None) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                if title is not None:
                    task.title = title
                if status is not None:
                    task.status = status
                self._save_tasks()
                return task
        return None

    def delete(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self._save_tasks()