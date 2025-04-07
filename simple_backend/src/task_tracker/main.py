import requests
from typing import Optional, Dict, List
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import json
from abc import ABC, abstractmethod

app = FastAPI()

# Конфигурация API
JSONBIN_API_KEY = "$2a$10$bLZ2aNVqrtMnHub27kLYvuG3E96w2QyE2bxl3CO22YcPWMY8I91zy"
JSONBIN_URL = "https://api.jsonbin.io/v3/b/67d01f2d8561e97a50e9e783"
LLM_API_URL = "https://api.cloudflare.com/client/v4/accounts/57ee70b4582d2b003a94cd3e16051019/ai/run/@cf/meta/llama-3.1-8b-instruct"
LLM_API_TOKEN = "0ukQ8LBkocp8QrUFvlhLcz8qQ2q0FUGXPbMGi2JI"

# Базовый класс для HTTP-клиентов
class BaseHTTPClient(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
        """Универсальный метод для выполнения HTTP-запросов."""
        url = f"{self.base_url}/{endpoint}"
        headers = headers or self.get_default_headers()
        print(f"Making {method} request to {url} with data {data}")
        response = requests.request(method, url, json=data, headers=headers)
        print(f"Response: {response.status_code} - {response.text}")
        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Resource not found")
        raise HTTPException(status_code=response.status_code, detail=f"Request failed: {response.text}")

    @abstractmethod
    def get_default_headers(self) -> Dict:
        """Абстрактный метод для получения заголовков по умолчанию."""
        pass

# Класс для работы с задачами через JSONBin
class JSONBinStorage(BaseHTTPClient):
    def __init__(self, url: str, api_key: str):
        super().__init__(url)
        self.api_key = api_key

    def get_default_headers(self) -> Dict:
        """Заголовки по умолчанию для JSONBin."""
        return {"X-Master-Key": self.api_key}

    def load_tasks(self) -> List[Dict]:
        response = self._make_request("GET", "")
        record = response.get("record", {})
        inner_record = record.get("record", {})
        return inner_record.get("tasks", [])

    def save_tasks(self, tasks: List[Dict]) -> None:
        headers = self.get_default_headers()
        headers["Content-Type"] = "application/json"  # Добавляем для PUT
        self._make_request("PUT", "", data={"record": {"tasks": tasks}}, headers=headers)

# Класс для работы с LLM API
class LLMClient(BaseHTTPClient):
    def __init__(self, api_url: str, api_token: str):
        super().__init__(api_url)
        self.api_token = api_token

    def get_default_headers(self) -> Dict:
        """Заголовки по умолчанию для LLMClient."""
        return {"Authorization": f"Bearer {self.api_token}", "Content-Type": "application/json"}

    def get_llm_response(self, prompt: str) -> str:
        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        response = self._make_request("POST", "", data=data)
        return response.get("result", {}).get("response", "No response from LLM")

# Модель задачи
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

# Инициализация клиентов
storage = JSONBinStorage(JSONBIN_URL, JSONBIN_API_KEY)
llm_client = LLMClient(LLM_API_URL, LLM_API_TOKEN)

# Эндпоинты FastAPI
@app.post("/tasks", response_model=Task)
async def create_task(request: Request):
    raw_body = await request.body()
    print(f"Raw request body: {raw_body}")
    body_str = raw_body.decode('utf-8')
    print(f"Decoded body: {body_str}")
    task_data = json.loads(body_str)
    task = Task(**task_data)
    print(f"Parsed task: {task}")
    llm_prompt = f"Explain how to solve the task: {task.title}. {task.description or ''}"
    print(f"LLM Prompt: {llm_prompt}")
    llm_response = llm_client.get_llm_response(llm_prompt)
    print(f"LLM Response: {llm_response}")
    task.description = f"{task.description or ''}\n\nLLM Suggestion: {llm_response}".strip()
    tasks = storage.load_tasks()
    print(f"Loaded tasks: {tasks}")
    tasks.append(task.dict())
    storage.save_tasks(tasks)
    print(f"Saved tasks: {tasks}")
    return task

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    tasks = storage.load_tasks()
    print(f"Retrieved tasks: {tasks}")
    return tasks