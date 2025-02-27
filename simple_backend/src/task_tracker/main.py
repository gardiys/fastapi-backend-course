import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

MOCKAPI_URL = "https://67b85410699a8a7baef39d0f.mockapi.io/api/v1/tasks/Tasks"

app = FastAPI()

# Файл для хранения задач
TASKS_FILE = "tasks.json"

# Pydantic-модель задачи
class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

# Получение всех задач
@app.get("/tasks", response_model=List[Task])
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    response = requests.get(MOCKAPI_URL)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=500, detail="Failed to fetch tasks")

# Создание новой задачи
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    response = requests.post(MOCKAPI_URL, json=task.dict())
    if response.status_code == 201:
        return response.json()
    raise HTTPException(status_code=500, detail="Failed to create task")

# Обновление задачи
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    response = requests.put(f"{MOCKAPI_URL}/{task_id}", json=updated_task.dict())
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=500, detail="Failed to update task")

# Удаление задачи
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    response = requests.delete(f"{MOCKAPI_URL}/{task_id}")
    if response.status_code == 200:
        return {"message": "Task deleted"}
    raise HTTPException(status_code=500, detail="Failed to delete task")
