from abc import ABC, abstractmethod
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import requests
from typing import List, Dict, Any, Optional  # Добавлен Optional
import os

app = FastAPI()

# Базовый HTTP клиент
class BaseHTTPClient(ABC):
    def __init__(self, base_url: str, headers: Dict[str, str]):
        self.base_url = base_url
        self.headers = headers
    
    def _make_request(self, method: str, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Общий метод для HTTP запросов"""
        url = f"{self.base_url}/{endpoint}".rstrip('/')
        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @abstractmethod
    def process_data(self, data: Any) -> Any:
        """Абстрактный метод для обработки данных"""
        pass

# Клиент для JSONBin.io
class JSONBinClient(BaseHTTPClient):
    def __init__(self):
        super().__init__(
            base_url="https://api.jsonbin.io/v3/b",
            headers={
                "Content-Type": "application/json",
                "X-Master-Key": os.getenv("JSONBIN_MASTER_KEY", "$2a$10$92anMMSpReZf03/15uRLVeWseU19ToTVWdu5qHUVY5p0M.uc9BNNq")
            }
        )
        self.bin_id = os.getenv("JSONBIN_BIN_ID", "686d63f08561e97a5033c303")
    
    def process_data(self, data: list) -> list:
        """Специфичная обработка для JSONBin"""
        return self._make_request("PUT", self.bin_id, payload=data)

# Клиент для Cloudflare AI
class CloudflareAIClient(BaseHTTPClient):
    def __init__(self):
        super().__init__(
            base_url="https://api.cloudflare.com/client/v4/accounts/edea76c52f70729758f024a33dd33d2e/ai/run",
            headers={
                "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_KEY', 'lsKqm_-Ugpodk4QA3OVM_gRfeKf-ixxezReGVueH')}",
                "Content-Type": "application/json"
            }
        )
        self.model = "@cf/meta/llama-2-7b-chat-int8"
    
    def process_data(self, prompt: str) -> str:
        """Специфичная обработка для Cloudflare AI"""
        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500
        }
        response = self._make_request("POST", self.model, payload=data)
        return response["result"]["response"]

# Модель задачи
class Task(BaseModel):
    original_text: str
    solution: str
    is_done: bool = False

# Инициализация клиентов
jsonbin_client = JSONBinClient()
ai_client = CloudflareAIClient()
tasks = []

@app.post("/tasks", response_model=List[Task])
async def create_task(text: str = Body(..., embed=True)):
    """Создание задачи с AI-решением"""
    solution = ai_client.process_data(text)
    
    new_task = {
        "original_text": text,
        "solution": solution,
        "is_done": False
    }
    
    tasks.append(new_task)
    jsonbin_client.process_data(tasks)
    
    return [new_task]

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)