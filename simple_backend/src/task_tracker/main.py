import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from cloudflare_ai import CloudflareTaskManager
from storage import TaskAPI

load_dotenv()
app = FastAPI()
base_task_api = TaskAPI(os.getenv('URL'))
cf_manager = CloudflareTaskManager()

class TaskCreate(BaseModel):
    title: str
    status: str = "pending"

@app.get("/tasks")
async def get_tasks():
    return await base_task_api.get_all()

@app.post("/tasks")
async def create_task(task_data: TaskCreate):
    task_data_dict = task_data.model_dump()

    try:
        ai_response = cf_manager.create_task(task_data.title)
        task_data_dict["ai_answer"] = ai_response.get("ai_solution", "No AI response")
        print(f"AI answer: {task_data_dict['ai_answer']}")
    except Exception as e:
        task_data_dict["ai_answer"] = f"AI error: {str(e)}"
        print(f"AI processing failed: {str(e)}")

    task = await base_task_api.create(task_data_dict)
    return task

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, updated_task: TaskCreate):
    return await base_task_api.update(task_id, updated_task.model_dump())

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    return await base_task_api.delete(task_id)

if __name__ == "__main__":
    uvicorn.run("main:app")