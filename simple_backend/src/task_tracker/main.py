from fastapi import FastAPI
from models import TaskStorage, Cloudflare
import os, json

app = FastAPI()
task_storage = TaskStorage(url=os.getenv("TASK_URL"), headers=json.loads(os.getenv("TASK_HEADERS")))
llm_model = Cloudflare(url=os.getenv("LLM_URL"), headers=json.loads(os.getenv("LLM_HEADERS")))


@app.get("/tasks")
def get_tasks():
    data = task_storage.read_tasks()
    return {'List of tasks': data}


@app.post("/tasks")
def create_task(task):
    response = llm_model.ask_solution(task)
    solution = response['result']['response']
    index = task_storage.add_task(task, solution)
    return {'message': f'New task added. Assigned id: {index}'}


@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    if task_storage.update_task(task_id):
        return {'message': 'Task status update'}
    return {'message': 'Task not found'}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_storage.delete_task(task_id):
        return {'message': 'Task deleted'}
    return {'message': 'Task not found'}
