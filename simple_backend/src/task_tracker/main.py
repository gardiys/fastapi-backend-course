from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
from pathlib import Path
from file_storage import FileStorage


app = FastAPI()
storage = FileStorage()

# Путь к json файлу
TASK_FILE = Path(
    "C:\\Users\\sereg\\Desktop\\git_homework\\fastapi-backend-course\\simple_backend\\src\\task_tracker\\tasks.json")


class Task(BaseModel):
    id: int
    title: str
    status: str


class TaskCreate(BaseModel):
    title: str
    status: str = "pending"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None

# API
@app.get("/tasks", response_model=list[Task])
def get_tasks():
    """Возвращаем список задач"""
    return [Task(**task) for task in storage.read_tasks()]


@app.post("/tasks", response_model=Task)
def create_task(task_data: TaskCreate):
    """Создаем новую задачу"""
    tasks = storage.read_tasks()
    new_task = {
        "id": storage.get_next_id(tasks),
        "title": task_data.title,
        "status": task_data.status
    }
    tasks.append(new_task)
    storage.save_tasks(tasks)
    return Task(**new_task)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate):
    """Обновляет задачу"""
    tasks = storage.read_tasks()
    update = False

    for task in tasks:
        if task["id"] == task_id:
            if task_data.title is not None:
                task["title"] = task_data.title
            if task_data.status is not None:
                task["status"] = task_data.status
            update = True
            break
    
    if not update:
        raise HTTPException(status_code=404, detail="Task not found")
    
    storage.save_tasks(tasks)
    return Task(**task)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удаляет задачу"""
    tasks_data = storage.read_tasks()
    length = len(tasks_data)
    tasks_data = [task for task in tasks_data if task["id"] != task_id]
    
    if len(tasks_data) == length:
        raise HTTPException(status_code=404, detail="Task not found")
    
    storage.save_tasks(tasks_data)
    return {"message": "Task deleted successfully"}
