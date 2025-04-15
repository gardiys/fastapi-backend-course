import json
import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()  # Создаем приложение FastAPI

class BaseHTTPClient:   # Базовый класс для работы с HTTP-запросами
    def __init__(self, api_url: str, api_key: str = None):
        self.api_url = api_url  # URL-адрес API
        self.api_key = api_key  # Ключ доступа к API (если требуется)

    def post_data(self, endpoint: str, data: dict):     #Отправка POST-запроса с JSON-данными
        headers = {
            'Authorization': f'Bearer {self.api_key}' if self.api_key else '',
            'Content-Type': 'application/json'
        }
        response = requests.post(f"{self.api_url}{endpoint}", headers=headers, json=data)
        response.raise_for_status()  # Проверяем успешность запроса
        return response.json()  # Возвращаем ответ в формате JSON


class CloudFlareAPI(BaseHTTPClient):    # Класс для работы с Cloudflare Workers AI
    def run(self, model: str, inputs: list):     #Выполнение задачи через Cloudflare AI
        input_data = {"messages": inputs}  # Формируем данные для отправки
        return self.post_data(model, input_data)  # Отправляем запрос

class TaskStorage:  # Класс для работы с файлами
    def __init__(self, filename: str):
        self.filename = filename  # Название файла

    def load_tasks(self):   #Загрузка задач из файла
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                return [Task(**task) for task in json.load(file)]  # Преобразуем данные в объекты Task
        return []  # Если файла нет, возвращаем пустой список

    def save_tasks(self, tasks):    #Сохранение задач в файл
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([task.dict() for task in tasks], file, ensure_ascii=False, indent=4)  # Сохраняем задачи в JSON


class Task(BaseModel):  # Модели данных
    id: int  # Уникальный номер задачи
    title: str  # Название задачи
    status: bool = False  # Выполнена задача или нет (по умолчанию — False)

class TaskCreate(BaseModel):
    title: str  # Только название задачи (без ID и статуса)


storage = TaskStorage('tasks.json') # Инициализация хранилища задач

@app.get("/tasks")  # Получаем все задачи
def get_tasks():
    return storage.load_tasks()  # Возвращаем список всех задач

@app.post("/tasks")  # Создаем новую задачу
def create_task(task_data: TaskCreate):
    tasks = storage.load_tasks()  # Загружаем текущие задачи
    task_id = len(tasks) + 1 if not tasks else max(task.id for task in tasks) + 1  # Генерируем ID
    new_task = Task(id=task_id, title=task_data.title, status=False)  # Создаем новую задачу
    tasks.append(new_task)  # Добавляем новую задачу в список
    cloudflare_api = CloudFlareAPI(     # Работа с Cloudflare API
        api_url="https://api.cloudflare.com/client/v4/accounts/e959035eda5785e18c0c699884ac8b13/ai/run/",
        api_key="0vP-4yVrIoQjNe4qvjKwHfNVlZRCdjuOmnpm_Ovz"
    )
    inputs = [
        {"role": "system", "content": "You are a helpful assistant that explains how to solve tasks."},
        {"role": "user", "content": f"Explain how to solve the task: {task_data.title}"}
    ]
    llm_response = cloudflare_api.run("@cf/meta/llama-3-8b-instruct", inputs)  # Отправляем запрос в Cloudflare AI

    storage.save_tasks(tasks)  # Сохраняем задачи в файл

    return {
        "task": new_task,
        "llm_response": llm_response
    }

@app.put("/tasks/{task_id}")    # Обновляем существующую задачу по ID
def update_task(task_id: int, task_data: TaskCreate):
    tasks = storage.load_tasks()  # Загружаем текущие задачи
    for task in tasks:
        if task.id == task_id:  # Если нашли задачу с нужным ID
            task.title = task_data.title  # Меняем её название
            storage.save_tasks(tasks)  # Сохраняем изменения
            return task  # Возвращаем обновлённую задачу
    return {'error': 'Task not found'}  # Если не нашли — возвращаем сообщение об ошибке


@app.delete("/tasks/{task_id}")    # Удаляем задачу по ID
def delete_task(task_id: int):
    tasks = storage.load_tasks()  # Загружаем текущие задачи
    new_tasks = [task for task in tasks if task.id != task_id]  # Убираем задачу с нужным ID
    if len(new_tasks) == len(tasks):
        return {"message":"Task deleted"}  # Если ничего не удалили, значит задача не найдена
    storage.save_tasks(new_tasks)  # Сохраняем обновлённый список задач
    return {"message": "Task deleted"}  # Возвращаем сообщение об успешном удалении