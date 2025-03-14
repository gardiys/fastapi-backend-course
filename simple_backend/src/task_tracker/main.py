from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class Task(BaseModel):
    name: str
    status: str

    def __repr__(self):
        return self.name


tasks: Dict[int, Task] = {}

@app.get("/tasks")
def get_tasks():
    return list(tasks.values())

@app.post("/tasks")
def create_task(task: Task):
    task_id = max(tasks, default=0) + 1
    tasks[task_id] = task
    return {'id': task_id, **task.dict()}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail='task not found')
    tasks[task_id] = task
    return {'id': task_id, **task.dict()}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail='task not found')
    del tasks[task_id]
    return 'task deleted'


