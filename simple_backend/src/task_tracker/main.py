from fastapi import FastAPI , status
from json_db import Json_db

app = FastAPI()
json_db = Json_db("data.json")



@app.get("/tasks")
def get_tasks() -> dict:

    return json_db.json_get_task()

@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_task(task_id:str,task_name: str ,status_task:str) -> str :

    return json_db.json_create_task(task_id, task_name, status_task)

@app.put("/tasks/{task_id}")
def update_task(task_id: str,task_name: str, status_task: str) -> str :

    return json_db.json_update_task(task_id, task_name, status_task)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str) -> str:

    return json_db.json_delete_task(task_id)
