import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi import FastAPI, HTTPException
from typing import List
from task_tracker.models import Task
from task_tracker.llm_client import CloudflareLLMClient
from task_tracker.task_storage import RemoteTaskStorage
from dotenv import load_dotenv
load_dotenv()

bin_id = os.getenv("BIN_ID")
api_key = os.getenv("API_KEY")
cloudflare_url = os.getenv("CLOUDFLARE_URL")

app = FastAPI()
storage = RemoteTaskStorage(bin_id=bin_id, api_key=api_key)
llm = CloudflareLLMClient(cloudflare_url)




@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return await storage.get_all()

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    try:
        solution = await llm.get_solution(task.name)
        task.name += f"\n\n Решение от ИИ: \n{solution}"
        await storage.add(task)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated: Task):
    result = await storage.update(task_id, updated)
    if result:
        return result
    raise HTTPException(status_code=404, detail="задача не найдена")    

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    result = await storage.delete(task_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="задача не найдена")    


