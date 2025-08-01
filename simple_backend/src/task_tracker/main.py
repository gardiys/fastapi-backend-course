from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from storage import RemoteTaskStorage

BIN_ID = "688cb14d7b4b8670d8aaf14a"
API_KEY = "$2a$10$v3HOV0RsRkMqIqCer9yP2OIsWM/6k3GCjmIwBYDwTxdUSeKrFMr9S"

app = FastAPI()
storage = RemoteTaskStorage(BIN_ID, API_KEY)

class Task(BaseModel):
    id: int
    title: str
    status: str

@app.get("/tasks")
def get_tasks():
    return storage.load()

@app.post("/tasks")
def create_task(task: Task):
    tasks = storage.load()
    if any(t["id"] == task.id for t in tasks):
        raise HTTPException(status_code=400, detail="Task with this ID already exists")
    tasks.append(task.dict())
    storage.save(tasks)
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    tasks = storage.load()
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks[i] = updated_task.dict()
            storage.save(tasks)
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = storage.load()
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            del tasks[i]
            storage.save(tasks)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
