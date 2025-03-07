from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

# URL хранилища JSONBin.io
API_URL = "https://api.jsonbin.io/v3/b/67cb2c8ce41b4d34e4a280c7"
API_KEY = "$2a$10$tfgkzYycm.XCF5y4PUhftuNyugbJjVI4WZlK0CfHQf1EnUac6gjvy"  # Добавь сюда свой API-ключ

HEADERS = {
    "X-Master-Key": API_KEY,  # Указываем API-ключ для авторизации
    "Content-Type": "application/json",
}


def load_tasks():
    """Загружает задачи из JSONBin.io."""
    try:
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()  # Загружаем JSON-объект
        return data.get("tasks", [])  # Извлекаем список задач
    except requests.RequestException as e:
        print(f"Ошибка загрузки данных: {e}")
        return []


def save_tasks():
    """Сохраняет задачи в JSONBin.io."""
    try:
        response = requests.put(API_URL, json=tasks, headers=HEADERS)
        response.raise_for_status()  # Проверяем успешность запроса
    except requests.RequestException as e:
        print(f"Ошибка сохранения данных: {e}")  # Логируем ошибку


# Загружаем задачи при старте сервера
tasks = load_tasks()

# Устанавливаем корректный ID для новых задач
task_id_counter = max((task["id"] for task in tasks), default=0) + 1


class Task(BaseModel):
    """Модель данных для задачи."""

    title: str
    status: str


@app.get("/tasks", response_model=List[dict])
def get_tasks():
    """Получить список всех задач."""
    return tasks


@app.post("/tasks", response_model=dict)
def create_task(task: Task):
    """Создать новую задачу."""
    global task_id_counter
    new_task = {"id": task_id_counter, "title": task.title, "status": task.status}
    tasks.append(new_task)
    task_id_counter += 1
    save_tasks()  # Сохраняем изменения
    return new_task


@app.put("/tasks/{task_id}", response_model=dict)
def update_task(task_id: int, updated_task: Task):
    """Обновить задачу по ID."""
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["status"] = updated_task.status
            save_tasks()  # Сохраняем изменения
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удалить задачу по ID."""
    global tasks
    updated_tasks = [task for task in tasks if task["id"] != task_id]

    if len(updated_tasks) == len(tasks):
        raise HTTPException(status_code=404, detail="Задача не найдена")

    tasks = updated_tasks
    save_tasks()  # Сохраняем изменения
    return {"message": "Задача удалена"}
