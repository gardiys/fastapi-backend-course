from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from jsonbin_client import JSONBinClient
from cloudflare_ai import CloudflareAI

app = FastAPI()
ai = CloudflareAI()
jsonbin = JSONBinClient()

tasks = jsonbin.load_tasks()
task_id_counter = max((task["id"] for task in tasks), default=0) + 1


class Task(BaseModel):
    """Модель данных для задачи."""

    title: str
    status: str


@app.get("/tasks", response_model=List[Dict])
def get_tasks():
    """Получить список всех задач."""
    return tasks


@app.post("/tasks", response_model=Dict)
def create_task(task: Task):
    global task_id_counter, tasks
    solution = ai.get_solution(task.title)  # Запрос к Cloudflare AI
    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "status": task.status,
        "solution": solution,
    }
    tasks.append(new_task)
    task_id_counter += 1
    jsonbin.save_tasks(tasks)
    return new_task


@app.put("/tasks/{task_id}", response_model=Dict)
def update_task(task_id: int, updated_task: Task):
    """Обновить задачу по ID."""
    global tasks
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["status"] = updated_task.status
            jsonbin.save_tasks(tasks)
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.delete("/tasks/{task_id}", response_model=Dict)
def delete_task(task_id: int):
    """Удалить задачу по ID."""
    global tasks
    updated_tasks = [task for task in tasks if task["id"] != task_id]
    if len(updated_tasks) == len(tasks):
        raise HTTPException(status_code=404, detail="Задача не найдена")
    tasks = updated_tasks
    jsonbin.save_tasks(tasks)
    return {"message": "Задача удалена"}
