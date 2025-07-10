from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from typing import List
import os

app = FastAPI()

# Модель данных
class Task(BaseModel):
    text: str
    solution: str = ""  # Добавляем поле для решения
    is_done: bool = False

# Конфигурация JSONBin.io
JSONBIN_MASTER_KEY = os.getenv("JSONBIN_MASTER_KEY", "$2a$10$92anMMSpReZf03/15uRLVeWseU19ToTVWdu5qHUVY5p0M.uc9BNNq")
JSONBIN_BIN_ID = os.getenv("JSONBIN_BIN_ID", "686fd88a6063391d31aaeb13")

headers = {
    'Content-Type': 'application/json',
    'X-Master-Key': JSONBIN_MASTER_KEY,
}

JSONBIN_URL = f'https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}'

# Конфигурация Cloudflare AI
CLOUDFLARE_API_KEY = os.getenv("CLOUDFLARE_API_KEY", "lsKqm_-Ugpodk4QA3OVM_gRfeKf-ixxezReGVueH")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "edea76c52f70729758f024a33dd33d2e")
MODEL_NAME = "@cf/meta/llama-2-7b-chat-int8"

class CloudflareAIClient:
    def __init__(self):
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run"
        self.headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_KEY}",
            "Content-Type": "application/json"
        }
    
    def get_solution(self, task_text: str) -> str:
        """Получаем решение задачи от AI"""
        prompt = (
            f"Пользователь создал задачу: '{task_text}'. "
            "Предложи 3 кратких способа решения этой задачи. "
            "Будь конкретным и используй маркированный список."
        )
        
        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/{MODEL_NAME}",
                headers=self.headers,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()["result"]["response"]
        except Exception as e:
            print(f"Cloudflare AI error: {str(e)}")
            return "Не удалось получить решение от AI"

# Инициализация клиентов
ai_client = CloudflareAIClient()

# Инициализация хранилища
try:
    response = requests.get(f"{JSONBIN_URL}/latest", headers=headers)
    tasks = [Task(**item) for item in response.json()['record']]
except Exception as e:
    print(f"Failed to load tasks from JSONBin: {str(e)}")
    tasks = []

@app.on_event("startup")
def verify_connection():
    try:
        # Проверяем подключение к JSONBin
        response = requests.get(
            JSONBIN_URL,
            headers={'X-Master-Key': JSONBIN_MASTER_KEY}
        )
        response.raise_for_status()
        print('✅ Подключение к JSONBin прошло успешно')
        
        # Проверяем подключение к Cloudflare AI
        test_response = ai_client.get_solution("test")
        if "Не удалось" not in test_response:
            print('✅ Подключение к Cloudflare AI прошло успешно')
        else:
            print('⚠️ Cloudflare AI подключен, но возвращает ошибки')
            
    except Exception as e:
        print("❌ Ошибка подключения:", str(e))
        raise

@app.get("/tasks", response_model=List[Task])
def list_tasks(limit: int = 10):
    print(tasks[:limit])
    return tasks[:limit]

@app.post("/tasks", response_model=Task)
def create_task(task_text: str):
    # Получаем решение от AI
    solution = ai_client.get_solution(task_text)
    
    # Создаем новую задачу
    new_task = Task(
        text=task_text,
        solution=solution,
        is_done=False
    )
    
    # Добавляем в локальное хранилище
    tasks.append(new_task)
    
    # Синхронизируем с JSONBin
    try:
        response = requests.put(
            JSONBIN_URL,
            json=[t.dict() for t in tasks],
            headers=headers
        )
        response.raise_for_status()
    except Exception as e:
        tasks.pop()  # Откатываем изменения при ошибке
        raise HTTPException(500, detail=f"Failed to save task: {str(e)}")
    
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    try:
        return tasks[task_id]
    except IndexError:
        raise HTTPException(404, detail='Task not found')

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        deleted_task = tasks.pop(task_id)
        
        # Синхронизируем с JSONBin
        response = requests.put(
            JSONBIN_URL,
            json=[t.dict() for t in tasks],
            headers=headers
        )
        response.raise_for_status()
        
        return {"status": "deleted", "task": deleted_task.dict()}
    except IndexError:
        raise HTTPException(404, detail='Task not found')
    except Exception as e:
        tasks.insert(task_id, deleted_task)  # Откатываем изменения
        raise HTTPException(500, detail=f"Failed to delete task: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)