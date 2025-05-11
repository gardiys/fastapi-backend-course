from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List
from CloudStorage import CloudStorage
from models import Task, CreateTask, UpdateTask, UserLogin
from auth import get_current_user, login, register, auth
from dotenv import load_dotenv
import os

load_dotenv()

BIN_URL = os.getenv("BIN_URL")
API_KEY = os.getenv("API_KEY")

if not BIN_URL or not API_KEY:
    raise RuntimeError("BIN_URL or API_KEY not found in enviroment")
storage = CloudStorage(BIN_URL, API_KEY)

app = FastAPI()
auth.handle_errors(app) #обработка ошибок

@app.post("/register")
def register_user(user: UserLogin):
    return register(user)

@app.post("/login")
def login_user(user: UserLogin):
    return login(user)


@app.get("/tasks", response_model=List[Task], dependencies=(Depends(get_current_user),))
def get_tasks(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    tasks = storage.load_tasks()
    return tasks[skip: skip + limit]


@app.post("/tasks", response_model=Task, dependencies=(Depends(get_current_user),))
def create_task(task_data: CreateTask):
    tasks = storage.load_tasks()
    new_id = max([task.id for task in tasks], default=0) + 1
    new_task = Task(id=new_id, **task_data.dict())
    tasks.append(new_task)
    storage.save_tasks(tasks)
    return new_task


@app.put("/tasks/{task_id}", response_model=Task, dependencies=(Depends(get_current_user),))
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


@app.delete("/tasks/{task_id}", response_model=Task, dependencies=(Depends(get_current_user),))
def delete_task(task_id: int):
    tasks = storage.load_tasks()
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            storage.save_tasks(tasks)
            return task
    raise HTTPException(status_code=404, detail="Task not found")
