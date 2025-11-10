from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from storage import JSONStorage, CloudJSONStorage
from models import Task
from config import settings
from clients import CloudFlareClient
from typing import List

app = FastAPI()
storage = CloudJSONStorage(bin_id=settings.BIN_ID, master_key=settings.MASTER_KEY)
client_ai = CloudFlareClient(settings.API_TOKEN_AI, settings.ACCOUNT_ID_AI)


@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc: ValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})



@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return storage.list_tasks()

@app.post("/tasks", response_model=Task)
def create_task(task_data: Task):
    ai_reply = client_ai.generate_answer(task_data.title)
    task_data.title = f"{task_data.title} — {ai_reply}"
    task = storage.create_task(task_data)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: Task):
    ai_reply = client_ai.generate_answer(task_data.title)
    task_data.title = f"{task_data.title} — {ai_reply}"
    task = storage.update_task(task_id, task_data)
    return task

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    task = storage.delete_task(task_id)
    return task