import sys
import os
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

sys.path.append(os.path.abspath("src"))
from jsonbin_storage import JSONBinStorage

app = FastAPI()

# Модель задачи
class Task(BaseModel):
    id: int
    title: str
    status: str = "в процессе"
    subtasks: List[str] = []

# Инициализация хранилища
storage = JSONBinStorage()

# Получить все задачи
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return storage.load_tasks()

# Создать новую задачу
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks = storage.load_tasks()
    tasks.append(task)
    storage.save_tasks(tasks)
    return task

# Обновить задачу
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    tasks = storage.load_tasks()
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = updated_task
            storage.save_tasks(tasks)
            return updated_task
    raise HTTPException(status_code=404, detail="Задача не найдена")

# Удалить задачу
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = storage.load_tasks()
    tasks = [task for task in tasks if task.id != task_id]
    storage.save_tasks(tasks)
    return {"message": "Задача удалена"}