from fastapi import FastAPI
from tracker import Task, TaskTracker


app = FastAPI()

tracker = TaskTracker()


@app.get("/tasks")
def get_tasks():
    return tracker.read_json()


@app.post("/tasks")
def create_task(task: Task):
    return tracker.add_json(task)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    return tracker.update_json(task_id, task)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return tracker.delete_json(task_id)

