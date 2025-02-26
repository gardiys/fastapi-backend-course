from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from typing import List
from cloudflare_ai import CloudflareAI

app = FastAPI()

CLOUDFLARE_ACCOUNT_ID = "21345cf5677943165e3b97e6be815b06"
CLOUDFLARE_API_TOKEN = "qq340bH1q3aZObneym0QNRgdiLJKda8euR8yQKu7"
API_URL = "https://67bed564b2320ee050118dfc.mockapi.io/tasks"

cloudflare_ai = CloudflareAI(CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN)

class Task(BaseModel):
    id: int
    title: str
    status: str
    solution: str = ""

class TaskCreate(BaseModel):
    title: str
    status: str = "todo"

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(API_URL)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    solution = await cloudflare_ai.generate_solution(task.title)
    if solution is None:
        solution = "Unable to generate solution at this time."

    task_with_solution = {
        "title": task.title,
        "status": task.status,
        "solution": solution
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(API_URL, json=task_with_solution)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: TaskCreate):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{API_URL}/{task_id}", json=task.dict())
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Task not found")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{API_URL}/{task_id}")
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Task not found")
            response.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")