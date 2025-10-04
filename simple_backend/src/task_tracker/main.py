import os
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, FastAPI
from rest_framework import status
from typing import Annotated
from task_model import Task, TaskAdd, TaskUpdate
from task_json_model import TasksJsonbin
from llm_model import LLMAssistant

app = FastAPI()
load_dotenv()

tasks = TasksJsonbin(
    api_key=os.getenv('JSONBIN_API_KEY'),
    bin_id=os.getenv('JSONBIN_BIN_ID')
)
llm_assistant = LLMAssistant(
    api_key=os.getenv('CLOUDFLARE_API_KEY'),
    llm_id=os.getenv('CLOUDFLARE_ACCOUNT_ID')
)


@app.get("/tasks")
def get_tasks():
    return tasks.get_all_tasks()


@app.post("/tasks")
def create_task(task: Annotated[TaskAdd, Depends()]):
    solution_llm = None
    if task.description != None:
        solution_llm = llm_assistant.request(task.description)
    obj = Task(**task.dict())
    obj.solution_llm = solution_llm
    tasks.add(obj)
    return f'Ok'


@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: Annotated[TaskUpdate, Depends()]):
    try:
        dct_up = {key: value for key, value in task.__dict__.items() if value != None}
        if dct_up.get('description') != None:
            solution_llm = llm_assistant.request(task.description)
            dct_up.setdefault('solution_llm', solution_llm)
        tasks.up_data(task_id, dct_up)
        return f'Ok'
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Задача с task_id {task_id} не найдена")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    try:
        tasks.delete(task_id)
        return 'Ok'
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Задача с ID {task_id} не найдена")
