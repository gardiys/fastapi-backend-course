import requests
from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

TASK_FILE = "tasks.json"
GITHUB_TOKEN = "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"
GIST_ID = "4cb4c4dd361a063120e71e46825c415e"


class Task:
    def __init__(self, id, title, status="To Do"):
        self.id = id
        self.title = title
        self.status = status


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
            if tasks_file:
                tasks_content = tasks_file["content"]
                if tasks_content:
                    tasks_data = json.loads(tasks_content)
                    tasks = []
                    max_id = 0
                    for task_data in tasks_data:
                        task = Task(
                            id=task_data["id"],
                            title=task_data["title"],
                            status=task_data["status"],
                        )
                        tasks.append(task)
                        if task.id > max_id:
                            max_id = task.id
                    return tasks
                else:
                    return []
            else:
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error loading tasks from Gist: {e}")
            return []

    def _save_tasks(self):
        headers = {"Authorization": f"token {self.github_token}"}
        gist_url = f"https://api.github.com/gists/{self.gist_id}"
        tasks_list_for_json = []
        for task in self.tasks:
            tasks_list_for_json.append(
                {"id": task.id, "title": task.title, "status": task.status}
            )
        payload = {
            "files": {
                "tasks.json": {"content": json.dumps(tasks_list_for_json, indent=4)}
            }
        }
        try:
            response = requests.patch(gist_url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error saving tasks to Gist: {e}")

    def _get_next_task_id(self):
        if not self.tasks:
            return 1
        else:
            return max(task.id for task in self.tasks) + 1

    def get_tasks(self):
        return [
            {"id": task.id, "title": task.title, "status": task.status}
            for task in self.tasks
        ]

    def create_task(self, task_data):
        new_task = Task(id=self.task_id_counter, title=task_data["title"])
        self.tasks.append(new_task)
        self._save_tasks()
        self.task_id_counter += 1
        return {"id": new_task.id, "title": new_task.title, "status": new_task.status}

    def update_task(self, task_id, task_data):
        for task in self.tasks:
            if task.id == task_id:
                if "title" in task_data:
                    task.title = task_data["title"]
                if "status" in task_data:
                    task.status = task_data["status"]
                self._save_tasks()
                return {"id": task.id, "title": task.title, "status": task.status}
        raise HTTPException(status_code=404, detail="Task not found")

    def delete_task(self, task_id):
        original_tasks_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        if len(self.tasks) == original_tasks_count:
            raise HTTPException(status_code=404, detail="Task not found")
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
