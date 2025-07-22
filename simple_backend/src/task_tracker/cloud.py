import requests
from schemas import Task

class CloudStorage:
    def __init__(self, bin_id: str, secret_key: str):
        self.url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        self.headers = {
            "X-Master-Key": secret_key,
            "Content-Type": "application/json"
        }

    def _read(self) -> list[Task]:
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        print("RESPONSE:", response.json())
        return [Task(**task) for task in response.json()["record"]]

    def _write(self, tasks: list[Task]):
        json_data = [task.model_dump() for task in tasks]
        response = requests.put(self.url, json=json_data, headers=self.headers)
        response.raise_for_status()

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