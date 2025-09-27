from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import requests
import json
import os
from typing import List
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Конфигурация JSONBin.io
JSONBIN_API_KEY = "$2a$10$pcwqDUhDIMDVaHFqqn4gCui92e3cFwdyhwt5gxmglbF.Y/FJAHDJG"
JSONBIN_BIN_ID = "68d56971d0ea881f408ac1f5"

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False
    ai_help: str = ''

class CloudTaskManager:
    def __init__(self, api_key: str, bin_id: str):
        self.api_key = api_key
        self.bin_id = bin_id
        self.url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        self.headers = {
            "Content-Type": "application/json",
            "X-Master-Key": api_key
        }
    
    def load_tasks(self) -> List[Task]:
        """Загрузить задачи из JSONBin.io"""
        response = requests.get(self.url, headers=self.headers)
        print(f"Статус ответа: {response.status_code}")  # Для отладки
        
        if response.status_code == 200:
            data = response.json()
            print(f"Полученные данные: {data}")  # Для отладки
            tasks_data = data['record']
            return [Task(**task) for task in tasks_data]                   
        elif response.status_code == 404:
            print("Бин не найден, создаем начальные задачи")
            return self._create_initial_tasks()
        else:
            print(f"Ошибка HTTP: {response.status_code}")
            return self._create_initial_tasks()

    
    def save_tasks(self, tasks: List[Task]) -> None:
        """Сохранить задачи в JSONBin.io"""
        try:
            data = [task.model_dump() for task in tasks]
            response = requests.put(self.url, json=data, headers=self.headers)
            
            if response.status_code == 200:
                print("Данные успешно сохранены")
            else:
                print(f"Ошибка сохранения: {response.status_code} - {response.text}")
                raise HTTPException(status_code=500, detail="Ошибка сохранения в облаке")
                
        except Exception as e:
            print(f"Ошибка: {e}")
            raise HTTPException(status_code=500, detail="Ошибка сохранения в облаке")
    
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
    
class CloudflareAI:
    def __init__(self):
        self.token = CLOUDFLARE_API_TOKEN
        self.account_id = CLOUDFLARE_ACCOUNT_ID
        self.url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/@cf/meta/llama-3.1-8b-instruct"
    

    async def get_ai_help(self, task_title: str) -> str:
        """Получить AI помощь для задачи"""
        try:
            print(f"Отправка запроса к Cloudflare AI...")
            print(f"URL: {self.url}")
            print(f"Токен: {self.token[:10]}...")  # Логируем только начало токена
            print(f"Account ID: {self.account_id}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.url,
                    headers={"Authorization": f"Bearer {self.token}"},
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
                
                print(f"Статус ответа: {response.status_code}")
                print(f"Текст ответа: {response.text}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"Полный ответ AI: {result}")
                    return result.get("result", {}).get("response", "Не удалось получить ответ")
                else:
                    print(f"Ошибка API: {response.status_code} - {response.text}")
                    return f"Ошибка API: {response.status_code}"
                    
        except Exception as e:
            print(f"Ошибка AI: {e}")
            return f"Ошибка подключения: {str(e)}"


# Создаем менеджер задач
task_manager = CloudTaskManager(JSONBIN_API_KEY, JSONBIN_BIN_ID)
ai_service = CloudflareAI()


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