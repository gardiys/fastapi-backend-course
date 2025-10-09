from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from task_tracker.gist_storage import GistStorage
from task_tracker.cloudflare_llm import CloudflareLLM

app = FastAPI()

storage = GistStorage()
llm = CloudflareLLM()

class TaskCreate(BaseModel):
    title: str
    status: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None

class Task(BaseModel):
    id: int
    title: str
    status: str
    solution: str


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return storage.load_data()


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    tasks = storage.load_data()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    solution = llm.get_solution(task.title)
    new_task = Task(
        id=new_id,
        title=task.title,
        status=task.status or "in work",
        solution=solution
    )
    tasks.append(new_task.dict())
    storage.save_data(tasks)
    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    tasks = storage.load_data()
    for i, task_dict in enumerate(tasks):
        if task_dict["id"] == task_id:
            updated_task = Task(
                id=task_id,
                title=task_update.title or task_dict["title"],
                status=task_update.status or task_dict["status"],
                solution=task_dict["solution"]
            )
            tasks[i] = updated_task.dict()
            storage.save_data(tasks)
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=200)
def delete_task(task_id: int):
    storage.delete_task_by_id(task_id)
    return
