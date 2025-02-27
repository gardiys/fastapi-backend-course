# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from task_manager import TaskManager, Task
from cloudflare_ai import CloudflareAI
from typing import List

app = FastAPI()

CLOUDFLARE_ACCOUNT_ID = "21345cf5677943165e3b97e6be815b06"
CLOUDFLARE_API_TOKEN = "qq340bH1q3aZObneym0QNRgdiLJKda8euR8yQKu7"
API_URL = "https://67bed564b2320ee050118dfc.mockapi.io/tasks"

cloudflare_ai = CloudflareAI(CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN)
task_manager = TaskManager(API_URL)

class TaskCreate(BaseModel):
    title: str
    status: str = "todo"

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return await task_manager.get_all()

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    solution = await cloudflare_ai.generate_solution(task.title)
    if solution is None:
        solution = "Unable to generate solution at this time."
    
    new_task = await task_manager.create(task.title, task.status, solution)
    if new_task is None:
        raise HTTPException(status_code=503, detail="Failed to create task")
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: TaskCreate):
    updated_task = await task_manager.update(task_id, task.title, task.status)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    await task_manager.delete(task_id)