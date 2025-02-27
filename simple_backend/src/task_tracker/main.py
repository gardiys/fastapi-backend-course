import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Файл для хранения задач
TASKS_FILE = "tasks.json"

# Pydantic-модель задачи
class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Получение всех задач
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return load_tasks()

# Создание новой задачи
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks = load_tasks()
    tasks.append(task.dict())
    save_tasks(tasks)
    return task

# Обновление задачи
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["completed"] = updated_task.completed
            save_tasks(tasks)
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# Удаление задачи
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    return {"message": "Task deleted"}
