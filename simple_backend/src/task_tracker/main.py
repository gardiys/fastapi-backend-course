from http.client import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests

from storage import CloudStorage

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    status: str

tasks = CloudStorage('$2a$10$3xXzKoQl9Akw7iQuxSY7Debk9qvfKv7cqkKJ9qUWURQKEQvy7j4Gq', '67db396b8561e97a50ef5ca1')

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """Получить все задачи."""
    return tasks.get_tasks()

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    """Создать новую задачу."""
    current_tasks = tasks.get_tasks()
    print("Полученные данные:", current_tasks)
    if not isinstance(current_tasks, list):
        current_tasks = []
    
    if any(t.get("id") == task.id for t in current_tasks):
        raise HTTPException(status_code=400, detail="Task with this ID already exists")
    
    current_tasks.append(task.model_dump())
    tasks.save_tasks(current_tasks)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    """Обновить информацию о задаче."""
    current_tasks = tasks.get_tasks()   
    for index, task in enumerate(current_tasks):
        if task["id"] == task_id:
            current_tasks[index] = updated_task.model_dump()
            tasks.save_tasks(current_tasks)
            return updated_task
    
    raise HTTPException(status_code=404, detail="Task not found")
    

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    """Удалить задачу."""
    current_tasks = tasks.get_tasks()
    for index, task in enumerate(current_tasks):
        if task["id"] == task_id:
            deleted_task = Task(**task)
            current_tasks.pop(index)
            tasks.save_tasks(current_tasks)
            return deleted_task
    
    raise HTTPException(status_code=404, detail="Task not found")
