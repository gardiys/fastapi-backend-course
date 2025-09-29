import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from cloud_storage import CloudTaskStorage
from cloud_flare import CloudflareAIClient

# Загружаем .env
load_dotenv()

app = FastAPI()

# Конфигурация
BIN_ID = os.getenv("JSONBIN_BIN_ID")
JSONBIN_API_KEY = os.getenv("JSONBIN_API_KEY")
CLOUDFLARE_AI_API_KEY = os.getenv("CLOUDFLARE_AI_API_KEY")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")

if not all([BIN_ID, JSONBIN_API_KEY, CLOUDFLARE_AI_API_KEY, CLOUDFLARE_ACCOUNT_ID]):
    raise RuntimeError("Не найдены необходимые переменные окружения")

# Инициализация клиентов
storage = CloudTaskStorage(BIN_ID, JSONBIN_API_KEY)
ai_client = CloudflareAIClient(CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_AI_API_KEY)


class Task(BaseModel):
    """Модель задачи"""

    id: int
    title: str
    status: str
    solution_advice: str = ""  # Новое поле для советов по решению


class TaskCreate(BaseModel):
    """Модель для создания задачи"""

    title: str
    status: str


@app.post("/tasks", response_model=Task)
async def create_task(task_data: TaskCreate):
    """Создание новой задачи с AI-анализом"""
    tasks = storage.load_tasks()
    new_id = max([task["id"] for task in tasks], default=0) + 1

    # Получаем советы от AI
    solution_advice = ai_client.get_task_solutions(task_data.title)

    # Создаем задачу с советами
    task = {
        "id": new_id,
        "title": task_data.title,
        "status": task_data.status,
        "solution_advice": solution_advice,
    }

    tasks.append(task)
    storage.save_tasks(tasks)
    return task


# Остальные endpoints остаются без изменений
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """Получение всех задач"""
    tasks = storage.load_tasks()
    return tasks


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskCreate):
    """Обновление задачи"""
    tasks = storage.load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = task_data.title
            task["status"] = task_data.status
            storage.save_tasks(tasks)
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удаление задачи"""
    tasks = storage.load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            storage.save_tasks(tasks)
            return {"message": "Задача удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")
