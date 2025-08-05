
from schemas import Task
from base_client import BaseHTTPClient


class CloudStorage(BaseHTTPClient):
    def __init__(self, bin_id: str, secret_key: str):
        url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        headers = {
            "X-Master-Key": secret_key,
            "Content-Type": "application/json"
        }
        super().__init__(url, headers)

    def _read(self) -> list[Task]:
        data = self.get()
        return [Task(**task) for task in data["record"]]

    def _write(self, tasks: list[Task]):
        json_data = [task.model_dump() for task in tasks]
        self.put(json_data)

    def get_all(self) -> list[Task]:
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

    def handle(self, *args, **kwargs):
        return self.get_all()