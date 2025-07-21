from fastapi import FastAPI
from http.client import HTTPException

from schemas import Task, TaskUpdate


app = FastAPI()

tasks: list[Task] = []

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, update_task: TaskUpdate):
    for index, task in enumerate(tasks):
        if task_id == task.id:
            tasks[index] = Task(
                id = task_id,
                title = update_task.title,
                status = update_task.status
            )
            return tasks[index]
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task_id == task.id:
            tasks.pop(index)
            return f"Task id={task_id} deleted"
    raise HTTPException(status_code=404, detail="Task not found")