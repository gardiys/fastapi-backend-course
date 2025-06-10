from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import json
from pathlib import Path
from cloud_storage import JsonBinStorage

load_dotenv()

app = FastAPI()
storage = JsonBinStorage()


class Task(BaseModel):
    id: int
    title: str
    status: str


# API
@app.get("/tasks", response_model=list[Task])
def get_tasks():
    """Возвращаем список задач"""
    return [Task(**task) for task in storage.read_tasks()]


@app.post("/tasks", response_model=Task)
def create_task(title: str, status: str = "pending"):
    """Создаем новую задачу"""
    tasks = storage.read_tasks()
    new_task = {
        "id": storage.get_next_id(tasks),
        "title": title,
        "status": status
    }
    tasks.append(new_task)
    storage.save_task(tasks)
    return Task(**new_task)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, title: Optional[str] = None, status: Optional[str] = None):
    """Обновляет задачу"""
    tasks = storage.read_tasks()

    for task in tasks:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if status is not None:
                task["status"] = status
            storage.save_task(tasks)
            return Task(**task)
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удаляет задачу"""
    tasks = storage.read_tasks()
    length = len(tasks)
    tasks_data = [task for task in tasks if task["id"] != task_id]

    if len(tasks_data) == length:
        raise HTTPException(status_code=404, detail="Task not found")

    storage.save_task(tasks)
    return {"message": "Task deleted successfully"}
