import json
from fastapi import HTTPException
from typing import List, Optional
from pydantic import BaseModel
from itertools import count
from pathlib import Path

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    status: str = "to do"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None


class JsonTasks:
    def __init__(self, filename: Path):
        self.file = filename
        if not self.file.exists():
            self._write([])

        tasks = self.get_all()
        last_id = max((task.id or 0 for task in tasks), default=0)
        self._id_counter = count(last_id + 1)
    
    def _write(self, tasks: List[Task]) -> None:
        with self.file.open("w", encoding="utf-8") as file:

            json.dump([task.model_dump() for task in tasks], file, indent=2, ensure_ascii=False)

    def get_all(self) -> List[Task]:
        with self.file.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
            return [Task(**task) for task in tasks]
        
    def add(self, task: Task) -> Task:
        tasks = self.get_all()
        task.id = next(self._id_counter)
        tasks.append(task)
        self._write(tasks)
        return task

    def update(self, task_id: int, task_update: TaskUpdate) -> Task:
        tasks = self.get_all()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                if task_update.title is not None:
                    task.title = task_update.title
                if task_update.status is not None:
                    task.status = task_update.status
                tasks[i] = task
                self._write(tasks)
                return task
        raise HTTPException(status_code=404, detail="Task not found")

    def delete(self, task_id: int) -> None:
        tasks = self.get_all()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                tasks.pop(i)
                self._write(tasks)
                return
        raise HTTPException(status_code=404, detail="Task not found")
