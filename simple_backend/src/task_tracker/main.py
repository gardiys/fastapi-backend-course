from fastapi import FastAPI
from async_task_tracker import GistStorage

app = FastAPI()
storage = GistStorage()


@app.get("/tasks")
async def get_tasks():
    return await storage.fetch()


@app.post("/tasks")
async def create_task(title: str):
    new_task = await storage.create_new_task(title)
    return {f'Task is created: {new_task}'}


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, title: str, status: int):
    update_t = await storage.update_task(task_id, title, status)
    if update_t is None:
        return {'Your task is not exist!'}
    return {f'Task is updated: {update_t}'}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    deleted = await storage.remove_task(task_id)
    if deleted is None:
        return 'Your task is not exist!'
    return {f'Task {deleted} was deleted!'}
