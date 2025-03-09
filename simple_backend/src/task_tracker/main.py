from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

# Файл для хранения данных
FILE_PATH = "tasks.json"


# Модель задачи
class Task(BaseModel):
    id: int
    title: str
    status: str


# Класс для работы с JSON-файлом
class TaskStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._load_tasks()

    def _load_tasks(self):
        if not os.path.exists(self.file_path):
            self.tasks = []
            self._save_tasks()
        else:
            try:
                with open(self.file_path, "r") as f:
                    self.tasks = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks = []

    def _save_tasks(self):
        print("Сохраняю задачи:", self.tasks)
        with open(self.file_path, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def get_tasks(self) -> List[dict]:
        return self.tasks if self.tasks else []


    def add_task(self, task: Task):
        self.tasks.append(task.dict())
        self._save_tasks()

    def update_task(self, task_id: int, updated_task: Task):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks[i] = updated_task.dict()
                self._save_tasks()
                return
        raise HTTPException(status_code=404, detail="Task not found")

    def delete_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self._save_tasks()


# Создаем объект хранилища
task_storage = TaskStorage(FILE_PATH)


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return task_storage.get_tasks()


@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    task_storage.add_task(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    task_storage.update_task(task_id, updated_task)
    return updated_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task_storage.delete_task(task_id)
    return {"message": "Task deleted"}
