from fastapi import FastAPI
from cloudflare_ai import CloudFlareConfig, CloudflareAI
from jsonbin_client import JSONBinConfig, JSONBinClient
from services import TaskManager, Task

app = FastAPI()

cloudflare_config = CloudFlareConfig()
jsonbin_config = JSONBinConfig()
ai = CloudflareAI(config=cloudflare_config)
storage_client = JSONBinClient(config=jsonbin_config)

task_manager = TaskManager(storage_client=storage_client, ai=ai)


@app.get("/tasks", response_model=list[dict])
def get_tasks():
    return task_manager.get_tasks()


@app.post("/tasks", response_model=dict)
def create_task(task: Task):
    return task_manager.add_task(task)


@app.put("/tasks/{task_id}", response_model=dict)
def update_task(task_id: int, updated_task: Task):
    return task_manager.update_task(task_id, updated_task)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return task_manager.delete_task(task_id)
