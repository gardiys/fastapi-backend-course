from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from task_storage import TaskStorage  
from config import get_settings
app = FastAPI()

settings = get_settings()
api_key = settings.JSONBIN_API_KEY
bin_id = settings.JSONBIN_BIN_ID

class Task(BaseModel):
    id: int
    title: str
    status: str


task_storage = TaskStorage(api_key=api_key,
                           bin_id=bin_id)

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    tasks = task_storage.load_tasks()
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks = task_storage.load_tasks()

    # Проверяем, существует ли уже задача с таким ID
    if any(t.get("id") == task.id for t in tasks):
        raise HTTPException(status_code=400, detail="Task with this ID already exists")

    task_dict = task.dict()
    tasks.append(task_dict)
    task_storage.save_tasks(tasks)

    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    tasks = task_storage.load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task.update(updated_task.dict())
            task_storage.save_tasks(tasks)
            return updated_task

    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = task_storage.load_tasks()

    updated_tasks = [task for task in tasks if task["id"] != task_id]

    if len(updated_tasks) == len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")

    task_storage.save_tasks(updated_tasks)
    return {"message": "Task deleted"}