import json
from typing import Any
from .base_http_client import BaseHTTPClient
from .config import settings
from fastapi import HTTPException

class GistStorage(BaseHTTPClient):
    def __init__(self):
        url = f"https://api.github.com/gists/{settings.GIST_ID}"
        super().__init__(token=settings.GITHUB_TOKEN, url=url)

    def load_data(self):
        gist_data = self.get()
        content = gist_data["files"]["tasks.json"]["content"]
        return json.loads(content)

    def save_data(self, tasks):
        updated_content = json.dumps(tasks, ensure_ascii=False, indent=2)
        payload = {"files": {"tasks.json": {"content": updated_content}}}
        return self.patch(payload)
    
    def delete_task_by_id(self,task_id: int) -> None:
        tasks = self.load_data()
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                tasks.pop(i)
                self.save_data(tasks)
                return
        raise HTTPException(status_code=404, detail="Task not found")
