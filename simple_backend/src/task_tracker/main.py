from fastapi import FastAPI, HTTPException, Path, Body
from pydantic import BaseModel
from typing import List, Optional
import requests
import os
from abc import ABC, abstractmethod

app = FastAPI()

# Конфигурация API
MOCKAPI_BASE_URL = "https://67b85410699a8a7baef39d0f.mockapi.io/api/v1/tasks/Tasks"
CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/accounts/c0444b3d36c2cc03c46a304589a12f35/ai/run/@cf/meta/llama-2-7b-chat-int8"
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "jZJcMYYtMOA64hhmUduk1axSYGhO-YqNbJX1vCmG")


# Абстрактный класс для HTTP-клиента
class BaseHTTPClient(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def request(self, method: str, endpoint: str, data: Optional[dict] = None, headers: Optional[dict] = None):
        """Универсальный метод для выполнения HTTP-запросов."""
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, json=data, headers=headers)

        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Resource not found")
        raise HTTPException(status_code=response.status_code, detail=f"Request failed: {response.text}")

    @abstractmethod
    def get(self, endpoint: str):
        pass

    @abstractmethod
    def post(self, endpoint: str, data: dict):
        pass

    @abstractmethod
    def put(self, endpoint: str, data: dict):
        pass

    @abstractmethod
    def delete(self, endpoint: str):
        pass


# Клиент для работы с MockAPI
class MockAPIClient(BaseHTTPClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def get(self, endpoint: str = ""):
        return self.request("GET", endpoint)

    def post(self, endpoint: str, data: dict):
        return self.request("POST", endpoint, data)

    def put(self, endpoint: str, data: dict):
        return self.request("PUT", endpoint, data)

    def delete(self, endpoint: str):
        return self.request("DELETE", endpoint)

    def fetch_tasks(self) -> List[dict]:
        return self.get("")

    def fetch_task(self, task_id: int) -> Optional[dict]:
        try:
            return self.get(f"/{task_id}")
        except HTTPException as e:
            if e.status_code == 404:
                return None
            raise

    def create_task(self, task: dict) -> dict:
        return self.post("", task)

    def update_task(self, task_id: int, updated_task: dict) -> dict:
        return self.put(f"/{task_id}", updated_task)

    def delete_task(self, task_id: int) -> dict:
        return self.delete(f"/{task_id}")


# Клиент для работы с Cloudflare Workers AI
class CloudflareLLMClient(BaseHTTPClient):
    def __init__(self, api_url: str, api_token: str):
        super().__init__(api_url)
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    def get(self, endpoint: str):
        raise NotImplementedError("GET не используется в Cloudflare LLM API")

    def post(self, endpoint: str, data: dict):
        return self.request("POST", endpoint, data, self.headers)

    def put(self, endpoint: str, data: dict):
        raise NotImplementedError("PUT не используется в Cloudflare LLM API")

    def delete(self, endpoint: str):
        raise NotImplementedError("DELETE не используется в Cloudflare LLM API")

    def get_llm_response(self, prompt: str) -> str:
        """Отправляет запрос в LLM и получает ответ."""
        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        }
        try:
            response = self.post("", data)
            return response.get("result", {}).get("response", "No response from LLM")
        except HTTPException as e:
            if e.status_code == 401:
                raise HTTPException(status_code=401, detail="Unauthorized: Check your API token or permissions")
            raise


# Инициализация клиентов
mockapi_client = MockAPIClient(MOCKAPI_BASE_URL)
cloudflare_ai = CloudflareLLMClient(CLOUDFLARE_API_URL, CLOUDFLARE_API_TOKEN)


# Pydantic модель задачи
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False


# Эндпоинты FastAPI
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return mockapi_client.fetch_tasks()


@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    llm_prompt = f"Explain how to solve the task: {task.title}. {task.description or ''}"
    llm_response = cloudflare_ai.get_llm_response(llm_prompt)
    task.description = f"{task.description or ''}\n\nLLM Suggestion: {llm_response}".strip()
    return mockapi_client.create_task(task.dict())


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int = Path(..., description="ID задачи для обновления"),
    updated_task: Task = Body(..., description="Новые данные задачи"),
):
    if not mockapi_client.fetch_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return mockapi_client.update_task(task_id, updated_task.dict())


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int = Path(..., description="ID задачи для удаления")):
    if not mockapi_client.fetch_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return mockapi_client.delete_task(task_id)
