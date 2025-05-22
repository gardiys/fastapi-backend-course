from fastapi import FastAPI , status
from json_db import Json_db


MASTER_API_KEY = "$2a$10$vS9hUcjtSMFHxBw0te7qcunwSZTMhK2Uwtt64GVJDUIdQU6g4sdw2"
BIN_API_KEY = "682ef8b48960c979a59f1cc0"

app = FastAPI()
json_db = Json_db(MASTER_API_KEY,BIN_API_KEY)


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
