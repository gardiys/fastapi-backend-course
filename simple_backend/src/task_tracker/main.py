from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks = []

class Task(BaseModel):
    id: int
    title: str
    status: str


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks")
def create_task(task):
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update_task: Task):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = update_task
            return update_task
    return {"error": "Task not found"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return {"message": "Task deleted"}
    return {"error": "Task not found"}
