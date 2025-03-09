from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import requests
import os
from cloudflare_ai import CloudflareAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

app = FastAPI()
ai = CloudflareAI()
API_KEY = os.getenv("JSONBIN_API_KEY")

if not API_KEY:
    raise ValueError(
        "API-ключ JSONBin.io не найден! Установите JSONBIN_API_KEY в .env."
    )

API_URL = "https://api.jsonbin.io/v3/b/67cb2c8ce41b4d34e4a280c7"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json",
}


def load_tasks():
    """Загружает список задач из JSONBin.io."""
    try:
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data.get("record", {}).get("record", [])  # Получаем список задач
    except requests.RequestException as e:
        return []


def save_tasks():
    """Сохраняет задачи в JSONBin.io."""
    global tasks
    try:
        requests.put(
            API_URL, json={"record": tasks}, headers=HEADERS
        ).raise_for_status()
    except requests.RequestException:
        pass  # Ошибки при сохранении не критичны


# Загружаем задачи при старте сервера
tasks = load_tasks()
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
    solution = ai.get_solution(task.title)  # Получаем ответ от Cloudflare AI
    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "status": task.status,
        "solution": solution,
    }
    tasks.append(new_task)
    task_id_counter += 1
    save_tasks()
    return new_task


@app.put("/tasks/{task_id}", response_model=Dict)
def update_task(task_id: int, updated_task: Task):
    """Обновить задачу по ID."""
    global tasks
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["status"] = updated_task.status
            save_tasks()
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
    save_tasks()
    return {"message": "Задача удалена"}
