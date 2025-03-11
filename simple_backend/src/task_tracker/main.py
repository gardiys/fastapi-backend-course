from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from cloudflare_ai import CloudflareAI
from jsonbin_client import JSONBinClient

app = FastAPI()
ai = CloudflareAI()


class TaskManager:
    """Класс для управления задачами."""

    def __init__(self, storage_client):
        self.storage_client = storage_client
        self.tasks = self.storage_client.load_tasks()

        if isinstance(self.tasks, dict) and "record" in self.tasks:
            self.tasks = self.tasks["record"]

        if not isinstance(self.tasks, list):
            raise ValueError("❌ Ошибка: self.tasks не является списком!")

        self.task_id_counter = max((task["id"] for task in self.tasks), default=0) + 1

    def add_task(self, task: "Task") -> Dict:
        """Добавляет новую задачу и сохраняет её в JSONBin."""
        solution = ai.get_solution(task.title)
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

    def get_tasks(self) -> List[Dict]:
        """Возвращает список задач."""
        return self.tasks

    def update_task(self, task_id: int, updated_task: "Task") -> Dict:
        """Обновляет задачу по ID."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["title"] = updated_task.title
                task["status"] = updated_task.status
                self.storage_client.save_tasks(self.tasks)  # Сохраняем изменения
                return task
        raise HTTPException(status_code=404, detail="Задача не найдена")

    def delete_task(self, task_id: int) -> Dict:
        """Удаляет задачу по ID."""
        filtered_tasks = [task for task in self.tasks if task["id"] != task_id]
        if len(filtered_tasks) == len(self.tasks):
            raise HTTPException(status_code=404, detail="Задача не найдена")

        self.tasks = filtered_tasks
        self.storage_client.save_tasks(self.tasks)  # Сохраняем изменения
        return {"message": "Задача удалена"}


task_manager = TaskManager(JSONBinClient())


class Task(BaseModel):
    """Модель данных для задачи."""

    title: str
    status: str


@app.get("/tasks", response_model=List[Dict])
def get_tasks():
    """Получить список всех задач."""
    return task_manager.get_tasks()


@app.post("/tasks", response_model=Dict)
def create_task(task: Task):
    """Создать новую задачу."""
    return task_manager.add_task(task)


@app.put("/tasks/{task_id}", response_model=Dict)
def update_task(task_id: int, updated_task: Task):
    """Обновить задачу."""
    return task_manager.update_task(task_id, updated_task)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удалить задачу."""
    return task_manager.delete_task(task_id)
