from fastapi import FastAPI
from typing import List
from model import Task
from savejson import SaveJsonDB
from simple_backend.src.task_tracker.сonfig import Config
from cloudflare_workers_ai import CloudflareWorkersAi

app = FastAPI()
config = Config()
AI_agent = config.get_ai_agent()

save_json_db = SaveJsonDB(config.get_url_DB(), 5)


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return save_json_db.load_tasks()


@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    task_ai = CloudflareWorkersAi(task, AI_agent, 5)
    task = task_ai.send_task_ai()
    return save_json_db.create_task(task)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    return save_json_db.update_task_id(task_id, updated_task)


@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    return save_json_db.delete_task_id(task_id)
