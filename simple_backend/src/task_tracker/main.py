from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os

from storage import FileStorage

from llm_client import CloudflareLLMClient

app = FastAPI()

storage = FileStorage()

API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")

try:
    if API_TOKEN and ACCOUNT_ID:
        llm_client = CloudflareLLMClient(API_TOKEN, ACCOUNT_ID)
        llm_enabled = True
    else:
        llm_client = None
        llm_enabled = False
        print("Cloudflare API ключи не найдены. LLM функциональность отключена.")
except Exception as e:
    llm_client = None
    llm_enabled = False
    print(f"Не удалось инициализировать LLM клиент: {e}")

class Task(BaseModel):
    id: str
    title: str
    status: str

@app.get("/")
def read_root():
    return {"message": "Task Tracker API"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    tasks_data = storage.load_tasks()
    return [Task(**task) for task in tasks_data]

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    if llm_enabled and llm_client:
        prompt = f"Объясни, как решить следующую задачу: {task.title}. Предложи пошаговое решение."
        
        llm_response = llm_client.ask_llm(prompt)
        
        if llm_response:
            task.title = f"{task.title}\n\nРешение от AI:\n{llm_response}"
        else:
            task.title = f"{task.title}\n\n(Не удалось получить решение от AI)"
    else:
        task.title = f"{task.title}\n\n(AI функциональность недоступна - проверьте настройки API)"
    
    tasks_data = storage.load_tasks()
    task_dict = task.model_dump()
    tasks_data.append(task_dict)
    storage.save_tasks(tasks_data)
    
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, updated_task: Task):
    tasks_data = storage.load_tasks()
    task_dict = updated_task.model_dump()
    for i, task in enumerate(tasks_data):
        if task["id"] == task_id:
            tasks_data[i] = task_dict
            storage.save_tasks(tasks_data)
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    tasks_data = storage.load_tasks()
    original_count = len(tasks_data)
    tasks_data = [task for task in tasks_data if task["id"] != task_id]
    
    if len(tasks_data) == original_count:
        raise HTTPException(status_code=404, detail="Task not found")
    
    storage.save_tasks(tasks_data)
    return {"message": "Task deleted"}

