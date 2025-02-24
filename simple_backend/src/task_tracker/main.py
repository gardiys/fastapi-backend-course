import requests
from fastapi import FastAPI, HTTPException
import json
import httpx

app = FastAPI()


class CloudflareLLM:
    def __init__(self, api_token: str, account_id: str):
        self.api_token = api_token
        self.account_id = account_id
        self.api_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/@cf/meta/llama-2-7b-chat-int8"

    def get_llm_explanation(self, task_text: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        data = {
            "prompt": f"Explain how to solve the following task: {task_text}. Provide a brief description of the solution."
        }
        try:
            response = httpx.post(
                self.api_url, headers=headers, json=data, timeout=10
            )  # Added timeout
            response.raise_for_status()
            return (
                response.json()
                .get("result", {})
                .get("response", "Failed to get an explanation from LLM.")
            )
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return f"Error when requesting LLM: {e}"
        except httpx.TimeoutException as e:
            print(f"Timeout error occurred: {e}")
            return "Request to LLM timed out."
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return f"Unexpected error when working with LLM: {e}"


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


class TaskFileManager:
    def __init__(self, gist_id, github_token):
        self.gist_id = gist_id
        self.github_token = github_token
        self.tasks = self._load_tasks()
        self.task_id_counter = self._get_next_task_id()

    def _load_tasks(self):
        headers = {"Authorization": f"token {self.github_token}"}
        gist_url = f"https://api.github.com/gists/{self.gist_id}"
        try:
            response = requests.get(gist_url, headers=headers)
            response.raise_for_status()
            gist_data = response.json()
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
        except requests.exceptions.RequestException:
            return []

    def _save_tasks(self):
        headers = {"Authorization": f"token {self.github_token}"}
        gist_url = f"https://api.github.com/gists/{self.gist_id}"
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
            response = requests.patch(gist_url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException:
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
                original_description = (
                    task.description
                )  # Сохраняем оригинальное описание
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
                            if (
                                original_description
                            ):  # Если оригинальное описание существовало, добавляем его
                                task.description += f"\n\n**Original Description:**\n{original_description}"

                if "status" in task_data:
                    task.status = task_data["status"]
                if "description" in task_data and "title" not in task_data:
                    task.description = task_data[
                        "description"
                    ]  # Обновляем описание только если title не менялся в запросе
                elif (
                    "description" in task_data and "title" in task_data
                ):  # Если description передан вместе с title, добавляем его к LLM описанию
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


task_file_manager = TaskFileManager(GIST_ID, GITHUB_TOKEN)


@app.get("/tasks")
async def get_tasks():
    return task_file_manager.get_tasks()


@app.post("/tasks")
async def create_task(task_data: dict):
    return task_file_manager.create_task(task_data)


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_data: dict):
    return task_file_manager.update_task(task_id, task_data)


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    return task_file_manager.delete_task(task_id)
