from storage import TaskAPI
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
task_api = TaskAPI()

class TaskCreate(BaseModel):
    title: str
    status: str = "pending"

@app.get("/tasks")
async def get_tasks():
    return await task_api.get_all()

@app.post("/tasks")
async def create_task(task_data: TaskCreate):
    return await task_api.create(task_data.model_dump())

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, updated_task: TaskCreate):
    return await task_api.update(task_id, updated_task.model_dump())

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    return await task_api.delete(task_id)

if __name__ == "__main__":
    uvicorn.run("main:app")
