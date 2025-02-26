from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from typing import List

app = FastAPI()
API_URL = "https://67bed564b2320ee050118dfc.mockapi.io/tasks"

class Task(BaseModel):
    id: int
    title: str
    status: str

class TaskCreate(BaseModel):
    title: str
    status: str

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        return response.json()

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=task.dict())
        return response.json()

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: TaskCreate):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{API_URL}/{task_id}", json=task.dict())
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Task not found")
        return response.json()

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{API_URL}/{task_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Task not found")
    return