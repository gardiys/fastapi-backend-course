from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
from pathlib import Path


app = FastAPI()

# Путь к json файлу
TASK_FILE = Path(
    "C:\\Users\\sereg\\Desktop\\git_homework\\fastapi-backend-course\\simple_backend\\src\\task_tracker\\tasks.json")


class Task(BaseModel):
    id: int
    title: str
    status: str

# Функции работы с json файлом
def load_tasks() -> list[Task]:
    """Загружаем задачи из файла"""
    if not TASK_FILE.exists():
        return []
    try:
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except(json.JSONDecodeError, FileNotFoundError):
        return []


def save_task(tasks_data):
    """Сохраняем задачи в файл"""
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=2)


def get_next_id() -> int:
    """Возвращает слещующий ID"""
    tasks = load_tasks()
    return max(task["id"] for task in tasks) + 1 if tasks else 1


# API
@app.get("/tasks", response_model=list[Task])
def get_tasks():
    """Возвращаем список задач"""
    return [Task(**task) for task in load_tasks()]


@app.post("/tasks", response_model=Task)
def create_task(title: str, status: str = "pending"):
    """Создаем новую задачу"""
    tasks_data = load_tasks()
    new_task = {"id": get_next_id(), "title": title, "status": status}
    tasks_data.append(new_task)
    save_task(tasks_data)
    return Task(**new_task)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, title: Optional[str] = None, status: Optional[str] = None):
    """Обновляет информацию о задаче"""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if status is not None:
                task["status"] = status
            return Task(**task)
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удаляет задачу"""
    tasks_data = load_tasks()
    length = len(tasks_data)
    tasks_data = [task for task in tasks_data if task["id"] != task_id]
    if len(tasks_data) == length:
        raise HTTPException(status_code=404, detail="Task not found")
    save_task(tasks_data)
    return {"message": "Task deleted successfully"}
