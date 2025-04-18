from fastapi import FastAPI
from pydantic import BaseModel

from jsonbin_storage import JsonBinStorage, StatusTask
from llm_client import LLMClient
from config import settings


app = FastAPI()
storage = JsonBinStorage(
    api_key=settings.jsonbin_api_key, bin_id=settings.jsonbin_bin_id
)
llm = LLMClient(
    api_key=settings.cloudflare_api_key, account_id=settings.cloudflare_account_id
)


class TaskCreate(BaseModel):
    task_text: str
    status: StatusTask = StatusTask.NEW


class TaskUpdate(BaseModel):
    task_text: str | None = None
    status: StatusTask | None = None


class TaskResponse(BaseModel):
    id: int
    task: str
    status: StatusTask


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks() -> list:
    return storage.get_all()


@app.post("/tasks", response_model=TaskResponse)
def create_task(data: TaskCreate):
    explanation = llm.ask(data.task_text)

    if explanation:
        full_text = f"{data.task_text}\n\n ИИ: {explanation}"
    else:
        full_text = data.task_text

    return storage.create(full_text, data.status)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate):
    return storage.update(task_id, data.task_text, data.status)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return storage.delete(task_id)
