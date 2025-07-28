from fastapi import FastAPI,HTTPException
from typing import List
from model import Task
from SaveJson import Save_Json, SaveJsonDB
from СloudflareWorkersAI import CloudflareWorkersAi

app = FastAPI()
AI_agent  = {"API_BASE_URL":"https://api.cloudflare.com/client/v4/accounts/f901bd0d9efbd69cdeec4c4e1b5f6e61/ai/run/",
             "API_TOKEN":"1QBo1ggCU54a6GNkWio7Mshys6qsZ9TKsG-27UmV","model":"@cf/meta/llama-3-8b-instruct"}

save_json_db = SaveJsonDB('https://688719b8071f195ca97f3e74.mockapi.io/')


@app.get("/tasks",response_model=List[Task])
def get_tasks():
    return save_json_db.load_tasks()

@app.post("/tasks",response_model=Task)
def create_task(task:Task):
    task_ai = CloudflareWorkersAi(task,AI_agent)
    task = task_ai.send_task_ai()
    return save_json_db.create_task(task)

@app.put("/tasks/{task_id}",response_model=Task)
def update_task(task_id: int,updated_task:Task):
    return save_json_db.update_task_id(task_id,updated_task)


@app.delete("/tasks/{task_id}",response_model=Task)
def delete_task(task_id: int):
    return save_json_db.delete_task_id(task_id)

