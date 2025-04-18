from base_http_client import BaseHTTPClient
from enum import Enum


class StatusTask(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class JsonBinStorage(BaseHTTPClient):
    def __init__(self, api_key: str, bin_id: str):
        base_url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        headers = {
            "X-Master-Key": api_key,
            "Content-Type": "application/json",
        }
        super().__init__(base_url=base_url, headers=headers)

    def parse_response(self, response):
        data = response.json().get("record")
        return data if isinstance(data, list) else []

    # def _read(self) -> list[dict]:
    #    response = requests.get(self.url, headers=self.headers)
    #    response.raise_for_status()
    #    return response.json()["record"]

    def _write(self, tasks: list[dict]) -> None:
        return self._request("PUT", json=tasks)

    def _find_task_index(self, tasks: list[dict], task_id: int) -> int | None:
        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                return index
        return None

    def get_all(self) -> list[dict]:
        return self._request("GET") or []

    def create(self, task_text: str, status: StatusTask = StatusTask.NEW) -> dict:
        tasks = self.get_all()
        new_id = max((x["id"] for x in tasks), default=0) + 1
        new_task = {"id": new_id, "task": task_text, "status": status.value}
        tasks.append(new_task)
        self._write(tasks)
        return new_task

    def update(
        self, task_id: int, text_task: str = None, status: StatusTask | None = None
    ) -> dict:
        tasks = self.get_all()
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
        tasks = self.get_all()
        index = self._find_task_index(tasks, task_id)
        if index is None:
            raise ValueError("Задача не найдена")

        deleted = tasks.pop(index)
        self._write(tasks)
        return {"message": "Задача удалена", "id": deleted["id"]}
