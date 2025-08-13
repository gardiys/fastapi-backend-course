import json
from typing import List
from pathlib import Path
from schemas import Task


class TaskJson:
    def __init__(self, file_name: str):
        self.file = Path(file_name)
        if not self.file.exists():
            self._write([])


    def _read(self) -> List[Task]:
        with self.file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return [Task(**item) for item in data]


    def _write(self, tasks: list[Task]):
        with self.file.open("w", encoding="utf-8") as f:
            json.dump([task.dict() for task in tasks], f, indent=2)


    def get_all(self) -> List[Task]:
        return self._read()


    def add(self, task: Task):
        tasks = self._read()
        tasks.append(task)
        self._write(tasks)


    def update(self, task_id: int, updated_task: Task):
        tasks = self._read()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                tasks[i] = Task(
                    id=task_id,
                    title=updated_task.title,
                    status=updated_task.status,
                )
                self._write(tasks)
                return
        raise ValueError("Task not found")


    def delete(self, task_id: int):
        tasks = self._read()
        for i, t in enumerate(tasks):
            if t.id == task_id:
                tasks.pop(i)
                self._write(tasks)
                return
        raise ValueError("Task not found")