from fastapi import FastAPI, HTTPException
from task_manager import TaskManager, Task
from typing import List

app = FastAPI()
task_manager = TaskManager()

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return task_manager.get_all()

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: Task):
    return task_manager.create(task.title, task.status)

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    updated_task = task_manager.update(task_id, task.title, task.status)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    task_manager.delete(task_id)
    return