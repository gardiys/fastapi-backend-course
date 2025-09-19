from fastapi import FastAPI, HTTPException
import requests
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv('.env')

class BaseHTTPClient(ABC):
    """Базовый класс для HTTP клиентов"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    @abstractmethod
    def get_headers(self) -> Dict[str, str]:
        """Абстрактный метод для получения заголовков"""
        pass
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Общий метод для HTTP запросов"""
        url = f"{self.base_url}/{endpoint}".rstrip('/')
        headers = self.get_headers()
        
        try:
            response = requests.request(
                method, 
                url, 
                headers=headers, 
                timeout=30,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise HTTPException(status_code=408, detail="Request timeout")
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500, 
                detail=f"HTTP error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

class CloudflareAI(BaseHTTPClient):
    """Клиент для работы с Cloudflare AI API"""
    
    def __init__(self):
        self.api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        self.model_name = "@cf/meta/llama-2-7b-chat-int8"
        super().__init__(f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run")
    
    def get_headers(self) -> Dict[str, str]:
        """Получение заголовков для Cloudflare API"""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def get_ai_suggestion(self, task_text: str) -> str:
        """Получает советы по решению задачи от LLM"""
        if not self.api_token or not self.account_id:
            return "⚠️ Cloudflare API не настроен"
        
        prompt = f"""
        Как эксперт по продуктивности, предложи 3 конкретных шага для решения этой задачи:
        "{task_text}"
        
        Ответь только списком шагов без лишних слов. Формат:
        1. Шаг первый
        2. Шаг второй  
        3. Шаг третий
        """
        
        payload = {
            "messages": [
                {"role": "system", "content": "Ты полезный ассистент по продуктивности."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300
        }
        
        try:
            result = self._make_request("POST", self.model_name, json=payload)
            return result['result']['response']
        except HTTPException as e:
            return f"❌ Ошибка Cloudflare AI: {e.detail}"
        except Exception as e:
            return f"❌ Неожиданная ошибка: {str(e)}"

class JSONBinIO(BaseHTTPClient):
    """Клиент для работы с JSONBin.io API"""
    
    def __init__(self):
        self.api_key = os.getenv('JSONBIN_API_KEY')
        self.bin_id = os.getenv('JSONBIN_BIN_ID')
        super().__init__("https://api.jsonbin.io/v3/b")
        
        if not self.bin_id:
            self.bin_id = self.create_new_bin()
    
    def get_headers(self) -> Dict[str, str]:
        """Получение заголовков для JSONBin API"""
        return {
            'Content-Type': 'application/json',
            'X-Master-Key': self.api_key,
            'X-Bin-Name': 'Task Manager Database'
        }
    
    def create_new_bin(self) -> str:
        """Создает новый bin на jsonbin.io"""
        initial_data = {"tasks": []}
        result = self._make_request("POST", "", json=initial_data)
        return result['metadata']['id']
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Получает все задачи из jsonbin.io"""
        try:
            result = self._make_request("GET", self.bin_id)
            return result['record'].get('tasks', [])
        except HTTPException:
            # Если файл поврежден, возвращаем пустой список
            return []
    
    def save_all_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Сохраняет все задачи в jsonbin.io"""
        self._make_request("PUT", self.bin_id, json={"tasks": tasks})

class DataBase:
    """Класс для работы с данными задач"""
    
    def __init__(self):
        self.__db_client = JSONBinIO()
        self.__ai_client = CloudflareAI()
    
    @property
    def get_task(self) -> List[Dict[str, Any]]:
        """Возвращает список всех задач"""
        try:
            tasks = self.__db_client.get_all_tasks()
            return tasks if tasks else []
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def create_task(self, text: str, status: bool = False) -> Dict[str, Any]:
        """Создает новую задачу с AI suggestions"""
        try:
            tasks = self.__db_client.get_all_tasks()
            
            # Генерация ID
            task_id = max((task.get('id', 0) for task in tasks), default=0) + 1
            
            # Получаем советы от AI
            ai_suggestions = self.__ai_client.get_ai_suggestion(text)
            
            # Создаем задачу
            new_task = {
                "id": task_id, 
                "text": f"{text}\n\n🎯 Советы по решению:\n{ai_suggestions}", 
                "status": status,

            }
            
            tasks.append(new_task)
            self.__db_client.save_all_tasks(tasks)
            
            return {
                "message": f"Task {task_id} created with AI suggestions!",
                "task_id": task_id,
                "ai_suggestions": ai_suggestions
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def update_task(self, task_id: int, text: str, status: bool) -> Dict[str, str]:
        """Обновляет задачу"""
        try:
            tasks = self.__db_client.get_all_tasks()
            
            for task in tasks:
                if task.get('id') == task_id:
                    task.update({"text": text, "status": status})
                    self.__db_client.save_all_tasks(tasks)
                    return {"message": f"Task {task_id} updated!"}
            
            raise HTTPException(status_code=404, detail=f"Task ID {task_id} not found")
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def delete_task(self, task_id: int) -> Dict[str, str]:
        """Удаляет задачу"""
        try:
            tasks = self.__db_client.get_all_tasks()
            
            for i, task in enumerate(tasks):
                if task.get('id') == task_id:
                    deleted_task = tasks.pop(i)
                    self.__db_client.save_all_tasks(tasks)
                    return {"message": f"Task {task_id} deleted!"}
            
            raise HTTPException(status_code=404, detail=f"Task ID {task_id} not found")
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Инициализация FastAPI
app = FastAPI()
db = DataBase()

# Эндпоинты
@app.get("/tasks")
def get_tasks():
    return db.get_task

@app.post("/tasks")
def create_task(text: str, status: bool = False):
    return db.create_task(text, status)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, text: str, status: bool):
    return db.update_task(task_id, text, status)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return db.delete_task(task_id)

