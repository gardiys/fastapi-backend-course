from fastapi import FastAPI, HTTPException
from utils import get, post, put, delete
from pydantic import BaseModel
from models import TaskCreate, TaskUpdate

app = FastAPI()


@app.get("/tasks")
def get_tasks():
    try:
        tasks = get()
        return tasks
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tasks")
def create_task(data: TaskCreate):
    if not data.name:
        return HTTPException(status_code=400, detail="Неверный формат данных")
    try:
        task = post(data.name)
        return task

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/tasks/{task_id}")
def update_task(task_id: str, data: TaskUpdate):
    if not data.name and not data.status:
        return HTTPException(status_code=400, detail="Неверный формат данных")
    try:
        task = put(task_id, data.name, data.status)
        return task

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    try:
        task = delete(task_id)
        return task

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
