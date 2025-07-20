import json
import os
from abc import ABC, abstractmethod
from typing import List

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

app = FastAPI()


class BaseHTTPClient(ABC):
    """Абстрактный базовый класс для HTTP-клиентов к внешним API."""

    @abstractmethod
    def _get_headers(self) -> dict:
        raise NotImplementedError

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        try:
            response = requests.request(
                method, url, headers=self._get_headers(), **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к {url}: {e}")
            raise HTTPException(
                status_code=503,
                detail=f"Внешний сервис недоступен: {e.__class__.__name__}",
            )


class TaskFileManager(BaseHTTPClient):
    """Клиент для работы с хранилищем задач jsonbin.io."""

    def __init__(self):
        """Инициализирует клиент, загружая конфигурацию для jsonbin.io."""
        self.api_key = os.getenv("JSONBIN_API_KEY")
        self.bin_id = os.getenv("JSONBIN_BIN_ID")
        self.base_url = f"https://api.jsonbin.io/v3/b/{self.bin_id}"

    def _get_headers(self) -> dict:
        """Реализация метода для получения заголовков, специфичных для jsonbin.io."""
        return {"X-Master-Key": self.api_key, "Content-Type": "application/json"}

    def read_tasks(self) -> List["Task"]:
        """Читает полный список задач из 'корзины' jsonbin.io."""
        try:
            response = self._make_request("get", self.base_url)
            data = response.json()
            task_data = data.get("record", [])
            return [Task(**task) for task in task_data]
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail="Не удалось обработать ответ от сервиса хранения.",
            )

    def write_tasks(self, tasks: List["Task"]):
        """Полностью перезаписывает список задач в 'корзине' jsonbin.io."""
        task_dicts = [task.dict() for task in tasks]
        self._make_request("put", self.base_url, json=task_dicts)


class CloudflareAIManager(BaseHTTPClient):
    """Клиент для работы с Cloudflare Workers AI."""

    def __init__(self):
        """Инициализирует клиент, загружая конфигурацию для Cloudflare AI."""
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.api_base_url = (
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"
        )
        self.model = "@cf/meta/llama-2-7b-chat-int8"

    def _get_headers(self) -> dict:
        """Реализация метода для получения заголовков аутентификации Cloudflare."""
        return {"Authorization": f"Bearer {self.api_token}"}

    def get_solution_for_task(self, task_title: str) -> str:
        prompt = (
            "Provide a brief, step-by-step plan to solve the following task. "
            "Do not add any introductions or conclusions, just the steps. "
            f"Task: '{task_title}'"
        )
        input_data = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that provides concise, "
                        "actionable steps to solve tasks."
                    ),
                },
                {"role": "user", "content": prompt},
            ]
        }
        url = f"{self.api_base_url}{self.model}"

        try:
            response = self._make_request("post", url, json=input_data)
            result = response.json()
            if (
                result.get("success")
                and "result" in result
                and "response" in result["result"]
            ):
                return result["result"]["response"].strip()
            else:
                print(f"Cloudflare AI returned an unsuccessful response: {result}")
                return ""
        except (HTTPException, json.JSONDecodeError) as e:
            print(f"Error calling Cloudflare AI API: {e}")
            return ""


manager = TaskFileManager()
cloudflare_manager = CloudflareAIManager()


class Task(BaseModel):
    """Модель задачи, которая хранится в системе и возвращается клиенту."""

    id: int
    title: str
    status: str


class TaskCreate(BaseModel):
    """Модель для создания новой задачи (клиент не передает id)."""

    title: str
    status: str


class TaskUpdate(BaseModel):
    """Модель для обновления существующей задачи."""

    title: str
    status: str


@app.get("/tasks")
def get_tasks() -> List[Task]:
    """Возвращает список всех задач."""
    return manager.read_tasks()


@app.post("/tasks")
def create_task(task: TaskCreate) -> Task:
    """Создает новую задачу, обогащая ее описание с помощью AI."""
    print(f"Getting solution for task: '{task.title}'")
    solution = cloudflare_manager.get_solution_for_task(task.title)
    enriched_title = task.title
    if solution:
        enriched_title += f"\n\n--- AI Suggested Steps ---\n{solution}"

    tasks = manager.read_tasks()
    new_id = max([t.id for t in tasks]) + 1 if tasks else 1
    new_task = Task(id=new_id, title=enriched_title, status=task.status)
    tasks.append(new_task)
    manager.write_tasks(tasks)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task_data: TaskUpdate) -> Task:
    """Обновляет задачу по ее ID."""
    tasks = manager.read_tasks()
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = Task(id=task_id, **updated_task_data.dict())
            manager.write_tasks(tasks)
            return tasks[i]
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict:
    """Удаляет задачу по ее ID."""
    tasks = manager.read_tasks()
    task_to_delete = next((task for task in tasks if task.id == task_id), None)
    if task_to_delete is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.remove(task_to_delete)
    manager.write_tasks(tasks)
    return {"message": "Task deleted successfully"}
