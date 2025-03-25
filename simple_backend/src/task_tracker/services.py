from fastapi import HTTPException
from pydantic import BaseModel
from cloudflare_ai import CloudflareAI
from jsonbin_client import JSONBinClient


class Task(BaseModel):

    title: str
    status: str


class TaskManager:

    def __init__(self, storage_client: JSONBinClient, ai: CloudflareAI):
        self.storage_client = storage_client
        self.ai = ai
        self.tasks = self.storage_client.load_tasks()

        if isinstance(self.tasks, dict) and "record" in self.tasks:
            self.tasks = self.tasks["record"]

        if not isinstance(self.tasks, list):
            raise ValueError(
                f"❌ Ошибка: self.tasks не является списком. Получено: {self.tasks}"
            )

        self.task_id_counter = max((task["id"] for task in self.tasks), default=0) + 1

    def add_task(self, task: Task) -> dict:

        solution = self.ai.get_solution(task.title)
        new_task = {
            "id": self.task_id_counter,
            "title": task.title,
            "status": task.status,
            "solution": solution,
        }

        self.tasks.append(new_task)
        self.task_id_counter += 1
        self.storage_client.save_tasks(self.tasks)
        return new_task

    def get_tasks(self) -> list[dict]:

        return self.tasks

    def update_task(self, task_id: int, updated_task: Task) -> dict:

        for task in self.tasks:
            if task["id"] == task_id:
                task["title"] = updated_task.title
                task["status"] = updated_task.status
                self.storage_client.save_tasks(self.tasks)
                return task
        raise HTTPException(status_code=404, detail="Задача не найдена")

    def delete_task(self, task_id: int) -> dict:
        """Удаляет задачу по ID."""
        filtered_tasks = [task for task in self.tasks if task["id"] != task_id]
        if len(filtered_tasks) == len(self.tasks):
            raise HTTPException(status_code=404, detail="Задача не найдена")

        self.tasks = filtered_tasks
        self.storage_client.save_tasks(self.tasks)
        return {"message": "Задача удалена"}
