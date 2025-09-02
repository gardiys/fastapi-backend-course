import json
import os
from task import Task, TaskUpdate
from typing import List, Dict


class TasksJson:

    def __init__(self, filename: str):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Убедиться, что файл существует, если нет - создать с пустым списком."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump([], file, indent=4)

    def _write_data(self, data: List[Dict]):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([task for task in data], file, indent=4)

    def _read_data(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _search_task(self, task_id: int, tasks: List[Dict]):
        for dct in tasks:
            if task_id == dct.get("id"):
                return dct
        raise KeyError(f"Задача с task_id {task_id} не найдена")

    def get_tasks(self):
        return [Task(**dct) for dct in self._read_data()]

    def add(self, task: Task):
        tasks = self._read_data()
        tasks.append(task.__dict__)
        self._write_data(tasks)

    def up_data(self, task_id: int, task: TaskUpdate):
        tasks = self._read_data()
        dct = self._search_task(task_id, tasks)
        dct_up = {key: value for key, value in task.__dict__.items() if value != None}
        dct.update(dct_up)
        self._write_data(tasks)

    def delete(self, task_id: int):
        tasks = self._read_data()
        dct = self._search_task(task_id, tasks)
        tasks.pop(tasks.index(dct))
        self._write_data(tasks)
