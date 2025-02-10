from fastapi import FastAPI, Body
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    text: str = "Description"
    status: bool = False


tasks_db = []


app = FastAPI()


@app.get("/tasks")
def get_tasks() -> list | str:
    if tasks_db:
        return tasks_db
    return "Tasks list is empty!"


@app.post("/tasks")
def create_task(task: Task) -> str:
    if tasks_db:
        task.id = max(tasks_db, key=lambda x: x.id).id + 1
    else:
        task.id = 0
    tasks_db.append(task)
    return "Task created!"


@app.put("/tasks/{task_id}")
def update_task(task_id: int, message: str = Body(), status: bool = Body()) -> str:
    if task_id <= len(tasks_db):
        changeable_task = tasks_db[task_id]
        changeable_task.text = message
        changeable_task.status = status
        return "Task changed!"
    return f"Task ID{task_id} is not in task list!"


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> str:
    if task_id <= len(tasks_db):
        tasks_db.pop(task_id)
        return f"Task ID{task_id} deleted!"
    return f"Task ID{task_id} is not in task list!"
