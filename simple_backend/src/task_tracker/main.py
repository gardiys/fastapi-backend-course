import os
from fastapi import FastAPI, HTTPException
from cloud_storage import CloudStorage
from storage import TaskStorage
from llm_client import LLMClient
from dotenv import load_dotenv

load_dotenv()

BIN_ID = os.getenv('BIN_ID')
API_KEY = os.getenv('API_KEY')

app = FastAPI()
store = CloudStorage(BIN_ID, API_KEY)
llm = LLMClient()
# store = TaskStorage('tasks.json')

# tasks = []
# tasks_counter = 1

@app.get("/tasks")
def get_tasks():
    return store.get_tasks()

@app.post("/tasks")
def create_task(task: dict):
    ai_hint = llm.get_task_solution(task['title'])
    task['solution'] = ai_hint
    return store.add_task(task)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: dict):
    updated = store.update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail='Task not found')
    return updated
            
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = store.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {'detail': 'Task deleted'}