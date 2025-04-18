from enum import Enum
import json
import os


class StatusTask(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskStorage:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path

    def _read(self) -> list[dict]:
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            return []
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, tasks: list[dict]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)

    def _find_task_index(self, tasks: list[dict], task_id: int) -> int | None:
        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                return index
        return None

    def get_all(self) -> list[dict]:
        tasks = self._read()
        return tasks

    def create(self, task_text: str, status: StatusTask = StatusTask.NEW) -> dict:
        tasks = self._read()
        new_id = max([x["id"] for x in tasks], default=0) + 1
        new_task = {"id": new_id, "task": task_text, "status": status.value}
        tasks.append(new_task)
        self._write(tasks)
        return new_task

    def update(
        self, task_id: int, text_task: str = None, status: StatusTask | None = None
    ) -> dict:
        tasks = self._read()
        index = self._find_task_index(tasks, task_id)

        if index is None:
            raise ValueError("Задача не найдена")
        if text_task is not None:
            tasks[index]["task"] = text_task
        if status is not None:
            tasks[index]["status"] = status.value

        self._write(tasks)
        return tasks[index]

    def delete(self, task_id: int) -> dict:
        tasks = self._read()
        index = self._find_task_index(tasks, task_id)
        if index is None:
            raise ValueError("Задача не найдена")

        tasks.remove(tasks[index])
        self._write(tasks)
        return {"message": "Задача удалена", "id": task_id}
