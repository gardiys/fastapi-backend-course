from fastapi import FastAPI
from task_tracker.models import Task
from task_tracker.storage import TaskStorage
from task_tracker.cloudflare_api import CloudflareClient
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
storage = TaskStorage()
llm_client = CloudflareClient()

@app.get("/tasks")
def get_tasks():
    pass

@app.post("/tasks")
def create_task(task: Task):
    solution = llm_client.get_solution(task.title)
    print(">>> SOLUTION:", solution)

    task.title = f"{task.title}\n\nSolution: {solution}"
    task.status = "new"
    created_task = storage.create_task(task)
    return created_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    pass

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    pass