from fastapi import FastAPI, HTTPException, Query, Response
from typing import List
from CloudStorage import CloudStorage
from models import Task, CreateTask, UpdateTask, UserLogin
from authx import AuthX
from auth import config
from dotenv import load_dotenv
import os

from cloudflare_ai import CloudflareLLM

load_dotenv()

BIN_URL = os.getenv("BIN_URL")
API_KEY = os.getenv("API_KEY")

storage = CloudStorage(BIN_URL, API_KEY)
llm = CloudflareLLM()

app = FastAPI()
security = AuthX(config=config)


@app.post("/login")
def login(creds: UserLogin, response: Response):
    if creds.username == "admin" and creds.password == "admin":
        token = security.create_access_token(uid="1234214")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")



@app.get("/tasks", response_model=List[Task])
def get_tasks(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    tasks = storage.load_tasks()
    return tasks[skip: skip + limit]


@app.post("/tasks", response_model=Task)
def create_task(task_data: CreateTask):
    tasks = storage.load_tasks()
    new_id = max([task.id for task in tasks], default=0) + 1
    
    #запрос к llm
    try:
        explanation = llm.solve_task(task_data.description)
        solution = explanation.get("response", "")
    except Exception as e:
        explanation = f"[Ошибка получения решения: {str(e)}]"
        
    new_task = Task(
        id=new_id, 
        description=task_data.description, 
        status=task_data.status,
        solution=solution
        )
    
    tasks.append(new_task)
    storage.save_tasks(tasks)
    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: UpdateTask):
    tasks = storage.load_tasks()
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_fields = task_data.dict(exclude_unset=True)
            updated_task = task.copy(update=updated_fields)
            tasks[index] = updated_task
            storage.save_tasks(tasks)
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    tasks = storage.load_tasks()
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            storage.save_tasks(tasks)
            return task
    raise HTTPException(status_code=404, detail="Task not found")
