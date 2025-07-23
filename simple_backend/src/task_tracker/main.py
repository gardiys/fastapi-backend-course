import os

from dotenv import load_dotenv
from fastapi import FastAPI
from http.client import HTTPException

from cloud import CloudStorage
from schemas import Task
from llm import LLMAssistant

load_dotenv()
app = FastAPI()

data = CloudStorage(
    bin_id=os.getenv("BIN_ID"),
    secret_key=os.getenv("SECRET_KEY")
)

llm = LLMAssistant(api_token=os.getenv("CLOUDFLARE_API_KEY"))

@app.get("/tasks")
def get_tasks():
    return data.get_all()

@app.post("/tasks")
def create_task(task: Task):
    solution = llm.task_llm(task.title)
    task.title += f"\n\n💡 Решение от LLM:\n{solution}"
    data.add(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, update_task: Task):
    try:
        data.update(task_id, update_task)
        return update_task
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        data.delete(task_id)
        return {"message": "Task deleted"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")