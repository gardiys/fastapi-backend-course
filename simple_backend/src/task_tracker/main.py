import requests
from fastapi import FastAPI, HTTPException
import json
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()


class BaseHTTPClient(ABC):
    @abstractmethod
    def _get_base_url(self):
        pass

    def _get_headers(self, additional_headers=None):
        base_headers = {}
        if additional_headers:
            base_headers.update(additional_headers)
        return base_headers

    def _handle_response(self, response):
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            raise HTTPException(
                status_code=response.status_code, detail=f"HTTP error: {e}"
            )
        except requests.exceptions.RequestException as e:
            print(f"Request exception: {e}")
            raise HTTPException(status_code=500, detail=f"Request exception: {e}")
        except json.JSONDecodeError:
            print("JSON decode error: Response is not valid JSON")
            raise HTTPException(
                status_code=500, detail="JSON decode error: Invalid JSON response"
            )
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    def _make_request(
        self, method, url_path, headers=None, params=None, json_data=None
    ):
        url = f"{self._get_base_url()}{url_path}"
        request_headers = self._get_headers(headers)
        try:
            response = requests.request(
                method, url, headers=request_headers, params=params, json=json_data
            )
            return self._handle_response(response)
        except HTTPException:
            raise
        except Exception as e:
            print(f"{method} request failed: {e}")
            raise HTTPException(status_code=500, detail=f"{method} request failed: {e}")

    def _get_request(self, url_path, headers=None, params=None):
        return self._make_request("GET", url_path, headers, params=params)

    def _post_request(self, url_path, headers=None, json_data=None):
        return self._make_request("POST", url_path, headers, json_data=json_data)

    def _patch_request(self, url_path, headers=None, json_data=None):
        return self._make_request("PATCH", url_path, headers, json_data=json_data)


class CloudflareLLM(BaseHTTPClient):
    def __init__(self, api_token, account_id):
        self.api_token = api_token
        self.account_id = account_id

    def _get_base_url(self):
        return f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/@cf/meta/llama-2-7b-chat-int8"

    def _get_headers(self, additional_headers=None):
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        return super()._get_headers(headers)

    def get_llm_explanation(self, task_text):
        data = {
            "prompt": f"Explain how to solve the following task: {task_text}. Provide a brief description of the solution."
        }
        try:
            response_data = self._post_request("", headers=None, json_data=data)
            return response_data.get("result", {}).get(
                "response", "Failed to get an explanation from LLM."
            )
        except HTTPException as e:
            return f"Error when requesting LLM: {e.detail}"


class TaskFileManager(BaseHTTPClient):
    def __init__(self, gist_id, github_token):
        self.gist_id = gist_id
        self.github_token = github_token
        self.tasks = self._load_tasks()
        self.task_id_counter = self._get_next_task_id()

    def _get_base_url(self):
        return f"https://api.github.com/gists/{self.gist_id}"

    def _get_headers(self, additional_headers=None):
        headers = {"Authorization": f"token {self.github_token}"}
        return super()._get_headers(headers)

    def _load_tasks(self):
        try:
            gist_data = self._get_request("", headers=None)
            tasks_file = gist_data["files"].get("tasks.json")
            if tasks_file and tasks_file["content"]:
                tasks_data = json.loads(tasks_file["content"])
                tasks = []
                max_id = 0
                for task_data in tasks_data:
                    task = Task(
                        id=task_data["id"],
                        title=task_data["title"],
                        status=task_data["status"],
                        description=task_data.get("description", ""),
                    )
                    tasks.append(task)
                    max_id = max(max_id, task.id)
                return tasks
            return []
        except HTTPException:
            return []

    def _save_tasks(self):
        tasks_list_for_json = [
            {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "description": task.description,
            }
            for task in self.tasks
        ]
        payload = {
            "files": {
                "tasks.json": {"content": json.dumps(tasks_list_for_json, indent=4)}
            }
        }
        try:
            self._patch_request("", headers=None, json_data=payload)
        except HTTPException:
            pass

    def _get_next_task_id(self):
        return max((task.id for task in self.tasks), default=0) + 1

    def get_tasks(self):
        return [
            {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "description": task.description,
            }
            for task in self.tasks
        ]

    def create_task(self, task_data):
        new_task = Task(
            id=self.task_id_counter,
            title=task_data["title"],
            description=task_data.get("description", ""),
        )
        if cloudflare_llm_client:
            llm_explanation = cloudflare_llm_client.get_llm_explanation(new_task.title)
            if llm_explanation:
                new_task.description += (
                    f"\n\n**Problem Solving Tip from LLM:**\n{llm_explanation}"
                )
        self.tasks.append(new_task)
        self._save_tasks()
        self.task_id_counter += 1
        return {
            "id": new_task.id,
            "title": new_task.title,
            "status": new_task.status,
            "description": new_task.description,
        }

    def update_task(self, task_id, task_data):
        for task in self.tasks:
            if task.id == task_id:
                if "title" in task_data:
                    self._update_task_title(
                        task, task_data
                    )  # Вызываем метод для обновления названия
                elif "description" in task_data:
                    self._update_task_description(
                        task, task_data
                    )  # Вызываем метод для обновления описания
                elif (
                    "status" in task_data
                ):  # Обрабатываем обновление статуса отдельно, без вложенности
                    task.status = task_data["status"]
                    self._save_tasks()
                    return self._serialize_task(
                        task
                    )  # Используем вспомогательный метод для сериализации
                else:
                    # Если нет ни title, ни description, ни status - ничего не обновляем, можно вернуть текущую задачу
                    return self._serialize_task(
                        task
                    )  # Возвращаем текущее состояние задачи

                self._save_tasks()
                return self._serialize_task(task)
        raise HTTPException(status_code=404, detail="Task not found")

    def _update_task_title(self, task, task_data):
        """Обновляет название задачи и получает подсказку от LLM, обновляя описание."""
        original_description = task.description
        task.title = task_data["title"]
        if cloudflare_llm_client:
            llm_explanation = cloudflare_llm_client.get_llm_explanation(task.title)
            if llm_explanation:
                task.description = (
                    f"**Problem Solving Tip from LLM:**\n{llm_explanation}"
                )
                if original_description:
                    task.description += (
                        f"\n\n**Original Description:**\n{original_description}"
                    )
        if (
            "description" in task_data
        ):  # Добавляем пользовательское описание после LLM подсказки
            if task.description:
                task.description += (
                    f"\n\n**User Provided Description:**\n{task_data['description']}"
                )
            else:
                task.description = (
                    f"**User Provided Description:**\n{task_data['description']}"
                )

    def _update_task_description(self, task, task_data):
        """Обновляет только описание задачи."""
        if "description" in task_data:
            task.description = task_data["description"]

    def _serialize_task(self, task):
        """Вспомогательный метод для сериализации объекта Task в словарь."""
        return {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "description": task.description,
        }

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self._save_tasks()
        return {"message": "Task deleted"}


TASK_FILE = "tasks.json"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GIST_ID = os.environ.get("GIST_ID")
CLOUDFLARE_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")

if CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID:
    cloudflare_llm_client = CloudflareLLM(CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID)
else:
    cloudflare_llm_client = None


class Task:
    def __init__(self, id, title, status="To Do", description=""):
        self.id = id
        self.title = title
        self.status = status
        self.description = description


task_file_manager = TaskFileManager(GIST_ID, GITHUB_TOKEN)


@app.get("/tasks")
async def get_tasks():
    return task_file_manager.get_tasks()


@app.post("/tasks")
async def create_task(task_data: dict):
    return task_file_manager.create_task(task_data)


@app.put("/tasks/{task_id}")
async def update_task(task_id, task_data: dict):
    return task_file_manager.update_task(task_id, task_data)


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    return task_file_manager.delete_task(task_id)
