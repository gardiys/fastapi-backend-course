import requests
from fastapi import FastAPI, HTTPException
import json
from abc import ABC, abstractmethod

app = FastAPI()


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

    def _get_request(self, url_path, headers=None, params=None):
        url = f"{self._get_base_url()}{url_path}"
        request_headers = self._get_headers(headers)
        try:
            response = requests.get(url, headers=request_headers, params=params)
            return self._handle_response(response)
        except HTTPException:
            raise
        except Exception as e:
            print(f"GET request failed: {e}")
            raise HTTPException(status_code=500, detail=f"GET request failed: {e}")

    def _post_request(self, url_path, headers=None, json_data=None):
        url = f"{self._get_base_url()}{url_path}"
        request_headers = self._get_headers(headers)
        try:
            response = requests.post(url, headers=request_headers, json=json_data)
            return self._handle_response(response)
        except HTTPException:
            raise
        except Exception as e:
            print(f"POST request failed: {e}")
            raise HTTPException(status_code=500, detail=f"POST request failed: {e}")

    def _patch_request(self, url_path, headers=None, json_data=None):
        url = f"{self._get_base_url()}{url_path}"
        request_headers = self._get_headers(headers)
        try:
            response = requests.patch(url, headers=request_headers, json=json_data)
            return self._handle_response(response)
        except HTTPException:
            raise
        except Exception as e:
            print(f"PATCH request failed: {e}")
            raise HTTPException(status_code=500, detail=f"PATCH request failed: {e}")


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
                original_description = task.description
                if "title" in task_data:
                    task.title = task_data["title"]
                    if cloudflare_llm_client:
                        llm_explanation = cloudflare_llm_client.get_llm_explanation(
                            task.title
                        )
                        if llm_explanation:
                            task.description = (
                                f"**Problem Solving Tip from LLM:**\n{llm_explanation}"
                            )
                            if original_description:
                                task.description += f"\n\n**Original Description:**\n{original_description}"

                if "status" in task_data:
                    task.status = task_data["status"]
                if "description" in task_data and "title" not in task_data:
                    task.description = task_data["description"]
                elif "description" in task_data and "title" in task_data:
                    if task.description:
                        task.description += f"\n\n**User Provided Description:**\n{task_data['description']}"
                    else:
                        task.description = f"**User Provided Description:**\n{task_data['description']}"

                self._save_tasks()
                return {
                    "id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "description": task.description,
                }
        raise HTTPException(status_code=404, detail="Task not found")

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self._save_tasks()
        return {"message": "Task deleted"}


TASK_FILE = "tasks.json"
GITHUB_TOKEN = "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"
GIST_ID = "4cb4c4dd361a063120e71e46825c415e"
CLOUDFLARE_API_TOKEN = "pwVCFw2m7Vs39_YNDeSNExGcDqZVKOz0CePfBMe3"
CLOUDFLARE_ACCOUNT_ID = "0260be9c395babb542118ae13f6a9a01"

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
