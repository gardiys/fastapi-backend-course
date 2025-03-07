import requests
from fastapi import FastAPI, HTTPException
import json
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import uuid
from pydantic import BaseModel, Field
from typing import Optional, List

load_dotenv()

app = FastAPI()


class Config:
    def __init__(self):
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.gist_id = os.environ.get("GIST_ID")
        self.cloudflare_api_token = os.environ.get("CLOUDFLARE_API_TOKEN")
        self.cloudflare_account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")


class BaseHTTPClient(ABC):
    @abstractmethod
    def _get_base_url(self):
        pass

    def _get_headers(self):
        return {}

    def _execute_request_and_handle_response(
        self, method, url_path, params=None, json_data=None
    ):
        url = f"{self._get_base_url()}{url_path}"
        request_headers = self._get_headers()
        try:
            response = requests.request(
                method, url, headers=request_headers, params=params, json=json_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = getattr(response, "status_code", 500)
            raise HTTPException(
                status_code=status_code,
                detail=f"HTTP ошибка: {e}, URL: {url}, Метод: {method}",
            )
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка декодирования JSON ответа: {e}, URL: {url}, Ответ: {getattr(response, 'text', 'Нет текста ответа')}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Неизвестная ошибка: {e}, URL: {url}, Метод: {method}",
            )

    def _get_request(self, url_path, params=None):
        return self._execute_request_and_handle_response("GET", url_path, params=params)

    def _post_request(self, url_path, json_data=None):
        return self._execute_request_and_handle_response(
            "POST", url_path, json_data=json_data
        )

    def _patch_request(self, url_path, json_data=None):
        return self._execute_request_and_handle_response(
            "PATCH", url_path, json_data=json_data
        )


class CloudflareLLM(BaseHTTPClient):
    def __init__(self, api_token, account_id):
        self.api_token = api_token
        self.account_id = account_id

    def _get_base_url(self):
        return f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/@cf/meta/llama-2-7b-chat-int8"

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def get_llm_explanation(self, task_text):
        data = {
            "prompt": f"Explain how to solve the following task: {task_text}. Provide a brief description of the solution."
        }
        try:
            response_data = self._post_request("", json_data=data)
            return response_data.get("result", {}).get(
                "response", "Failed to get an explanation from LLM."
            )
        except HTTPException as e:
            return f"Error when requesting LLM: {e.detail}"


class TaskCreate(BaseModel):
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: Optional[str] = Field(None, description="Task status")


class TaskResponse(BaseModel):
    id: str = Field(..., description="Task ID")
    title: str = Field(..., description="Task title")
    status: str = Field(..., description="Task status")
    description: Optional[str] = Field(None, description="Task description")


class Task(BaseModel):
    id: str = Field(..., description="Task ID")
    title: str = Field(..., description="Task title")
    status: str = Field("To Do", description="Task status")
    description: Optional[str] = Field("", description="Task description")


class TaskFileManager(BaseHTTPClient):
    def __init__(self, gist_id, github_token, cloudflare_llm_client=None):
        self.gist_id = gist_id
        self.github_token = github_token
        self.cloudflare_llm_client = cloudflare_llm_client
        self.tasks = self._load_tasks()

    def _enrich_task_with_llm_explanation(self, task: Task):
        if self.cloudflare_llm_client:
            llm_explanation = self.cloudflare_llm_client.get_llm_explanation(task.title)
            if llm_explanation:
                task.description += (
                    f"\n\n**Problem Solving Tip from LLM:**\n{llm_explanation}"
                )

    def _get_base_url(self):
        return f"https://api.github.com/gists/{self.gist_id}"

    def _get_headers(self):
        return {"Authorization": f"token {self.github_token}"}

    def _load_tasks(self):
        try:
            gist_data = self._get_request("")
            tasks_file = gist_data["files"].get("tasks.json")
            if tasks_file and tasks_file["content"]:
                tasks_data = json.loads(tasks_file["content"])
                tasks = []
                for task_data in tasks_data:
                    task_id = task_data.get("id")
                    if task_id is not None:
                        task_data["id"] = str(task_id)
                    tasks.append(Task(**task_data))
                return tasks
            return []
        except HTTPException:
            raise

    def _save_tasks(self):
        tasks_list_for_json = [task.dict() for task in self.tasks]
        payload = {
            "files": {
                "tasks.json": {"content": json.dumps(tasks_list_for_json, indent=4)}
            }
        }
        try:
            self._patch_request("", json_data=payload)
        except HTTPException:
            pass

    def get_tasks(self) -> List[TaskResponse]:
        return [TaskResponse(**task.dict()) for task in self.tasks]

    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        new_task = Task(
            id=str(uuid.uuid4()),
            title=task_data.title,
            description=task_data.description,
        )
        self._enrich_task_with_llm_explanation(new_task)
        self.tasks.append(new_task)
        self._save_tasks()
        return TaskResponse(**new_task.dict())

    def update_task(self, task_id: str, task_data: TaskUpdate) -> TaskResponse:
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        updated = False

        if task_data.title is not None:
            self._update_task_title(task, task_data)
            updated = True
        if task_data.description is not None:
            self._update_task_description(task, task_data)
            updated = True
        if task_data.status is not None:
            task.status = task_data.status
            updated = True

        if updated:
            self._save_tasks()
            return TaskResponse(**task.dict())

        return TaskResponse(**task.dict())

    def _update_task_title(self, task: Task, task_data: TaskUpdate):
        if task_data.title:
            task.title = task_data.title
        task.description = ""
        self._enrich_task_with_llm_explanation(task)

    def _update_task_description(self, task: Task, task_data: TaskUpdate):
        if task_data.description:
            task.description = task_data.description

    def delete_task(self, task_id: str):
        self.tasks = [task for task in self.tasks if task.id != str(task_id)]
        self._save_tasks()
        return {"message": "Task deleted"}


config = Config()

cloudflare_llm_client = None
if config.cloudflare_api_token and config.cloudflare_account_id:
    cloudflare_llm_client = CloudflareLLM(
        config.cloudflare_api_token, config.cloudflare_account_id
    )

task_file_manager = TaskFileManager(
    config.gist_id, config.github_token, cloudflare_llm_client
)


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    return task_file_manager.get_tasks()


@app.post("/tasks", response_model=TaskResponse)
def create_task(task_data: TaskCreate):
    return task_file_manager.create_task(task_data)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_data: TaskUpdate):
    return task_file_manager.update_task(task_id, task_data)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    return task_file_manager.delete_task(task_id)