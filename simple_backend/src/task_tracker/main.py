from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import requests
import json
import os
from typing import List, Any, Dict
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Конфигурация JSONBin.io
JSONBIN_API_KEY = "$2a$10$pcwqDUhDIMDVaHFqqn4gCui92e3cFwdyhwt5gxmglbF.Y/FJAHDJG"
JSONBIN_BIN_ID = "68d56971d0ea881f408ac1f5"

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")


class BaseHTTPClient:
    """Базовый класс для HTTP клиентов"""
    
    def __init__(self, base_url: str, headers: Dict[str, str] = None):
        self.base_url = base_url
        self.headers = headers or {}
    
    def _request_sync(self, method: str, endpoint: str = "", **kwargs) -> Any:
        """Синхронный HTTP запрос"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            print(f"HTTP {method} {url} - Status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка HTTP запроса: {e}")
            raise HTTPException(status_code=500, detail=f"Ошибка HTTP: {str(e)}")
    
    async def _request_async(self, method: str, endpoint: str = "", **kwargs) -> Any:
        """Асинхронный HTTP запрос"""
        url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, headers=self.headers, **kwargs)
                print(f"Async HTTP {method} {url} - Status: {response.status_code}")
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            print(f"Ошибка асинхронного HTTP запроса: {e}")
            raise HTTPException(status_code=500, detail=f"Ошибка HTTP: {str(e)}")

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False
    ai_help: str = ''

class CloudTaskManager(BaseHTTPClient):

    def __init__(self, api_key: str, bin_id: str):
        base_url = f"https://api.jsonbin.io/v3/b/{bin_id}"

        headers = {
            "Content-Type": "application/json",
            "X-Master-Key": api_key
        }

        super().__init__(base_url, headers)

        self.api_key = api_key
        self.bin_id = bin_id
    
    def load_tasks(self) -> List[Task]:
        """Загрузить задачи из JSONBin.io"""
        
        try:
            data = self._request_sync('GET')

            tasks_data = data['record']
            return [Task(**task) for task in tasks_data]
        except HTTPException:
            print("Бин не найден, создаем начальные задачи")
            return self._create_initial_tasks()
        


    
    def save_tasks(self, tasks: List[Task]) -> None:
        """Сохранить задачи в JSONBin.io"""
        data = [task.model_dump() for task in tasks]
        self._request_sync("PUT", json=data)
        print("Данные успешно сохранены")
    
    def _create_initial_tasks(self) -> List[Task]:
        """Создать начальные задачи если бин не существует"""
        print("Создаем начальные задачи...")
        initial_tasks_data = [
            {"id": 1, "title": "купить молоко", "completed": False, "ai_help": ""},
            {"id": 2, "title": "позавтракать", "completed": True, "ai_help": ""},
            {"id": 3, "title": "позвонить дедушке", "completed": False, "ai_help": ""}
        ]
        
        initial_tasks = [Task(**task) for task in initial_tasks_data]
        self.save_tasks(initial_tasks)
        return initial_tasks
    
    def get_next_id(self, tasks: List[Task]) -> int:
        """Получить следующий ID для новой задачи"""
        if not tasks:
            return 1
        return max(task.id for task in tasks) + 1
    
class CloudflareAI(BaseHTTPClient):
    """Клиент для Cloudflare AI"""
    
    def __init__(self, api_token: str, account_id: str, model: str = "@cf/meta/llama-3.1-8b-instruct"):
        base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        super().__init__(base_url, headers)
        self.model = model


    async def get_ai_help(self, task_title: str) -> str:
        """Получить AI помощь для задачи"""
        try:
            print(f"Отправка запроса к Cloudflare AI...")
            print(f"URL: {self.base_url}/{self.model}")  # ← Используем base_url из базового класса
            print(f"Токен: {self.headers['Authorization'][:10]}...")  # ← Токен из headers
            data = await self._request_async(
                "POST", 
                endpoint=f"/{self.model}",
                json={
                    "messages": [
                        {
                            "role": "user", 
                            "content": f"Кратко объясни как решить задачу: {task_title}"
                        }
                    ]
                },
                timeout=30.0
            )
            
            return data.get("result", {}).get("response", "Не удалось получить ответ")
                    
                    
        except Exception as e:
            print(f"Ошибка AI: {e}")
            return f"Ошибка подключения: {str(e)}"


# Создаем менеджер задач
task_manager = CloudTaskManager(JSONBIN_API_KEY, JSONBIN_BIN_ID)
ai_service = CloudflareAI(CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID)


async def add_ai_to_task(task_id: int, task_title: str):
    try:
        ai_help = await ai_service.get_ai_help(task_title)
        
        tasks = task_manager.load_tasks()
        for task in tasks:
            if task.id == task_id:
                task.ai_help = ai_help
                task_manager.save_tasks(tasks)
                print(f"Добавлена AI помощь для задачи {task_id}")
                break
    except Exception as e:
        print(f"Ошибка при добавлении AI помощи: {e}")

# Эндпоинты
@app.get("/tasks")
def get_tasks():
    return task_manager.load_tasks()

@app.post("/tasks")
async def create_task(title: str, background_tasks: BackgroundTasks):
    tasks = task_manager.load_tasks()
    new_id = task_manager.get_next_id(tasks)
    new_task = Task(id=new_id, title=title, completed=False)
    tasks.append(new_task)
    task_manager.save_tasks(tasks)

    background_tasks.add_task(add_ai_to_task, new_id, title)

    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, background_tasks: BackgroundTasks, title: str = None, completed: bool = None):
    tasks = task_manager.load_tasks()
    for task in tasks:
        if task.id == task_id:
            if title is not None:
                task.title = title
            if completed is not None:
                task.completed = completed
            task_manager.save_tasks(tasks)

            background_tasks.add_task(add_ai_to_task, task_id, title)

            return task
    return {"error": "Задача не найдена"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = task_manager.load_tasks()
    for i, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(i)
            task_manager.save_tasks(tasks)
            return {"message": f"Задача '{deleted_task.title}' удалена"}
    return {"error": "Задача не найдена"}

@app.on_event("startup")
async def startup_event():
    """Проверяем соединение при запуске"""
    print("Проверка соединения с JSONBin.io...")
    tasks = task_manager.load_tasks()
    print(f"Загружено задач: {len(tasks)}")