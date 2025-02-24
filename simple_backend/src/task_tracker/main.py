from fastapi import FastAPI
from pydantic import BaseModel


class Task(BaseModel):
    task_id: int
    task_name: str
    task_satus: str


app = FastAPI()

tasks = []
t_id = []


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return tasks


@app.post("/tasks")
def create_task(task: Task):
    if task.task_id in t_id:
        return f'Task-{task.task_id} already exists'
    t_id.append(task.task_id)
    tasks.append(task)
    return {f'Task-{task.task_id} has been created': task}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id in t_id and task_id == task.task_id:
        for t in tasks:
            if t.task_id == task.task_id:
                tasks.remove(t)
                tasks.append(task)
                return {f'An updated task-{task_id}': task}
    return 'Task update failed'


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id in t_id:
        for t in tasks:
            if task_id == t.task_id:
                tasks.remove(t)
                return f'Task-{task_id} has been deleted'
    return 'Task does not exist'
