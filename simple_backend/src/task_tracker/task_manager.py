# task_manager.py
from base_http_client import BaseHTTPClient
from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    id: int
    title: str
    status: str
    solution: str = ""

class TaskManager(BaseHTTPClient):
    def __init__(self, api_url: str = "https://67bed564b2320ee050118dfc.mockapi.io/tasks"):
        super().__init__()
        self.api_url = api_url

    async def perform_action(self, action: str, task_id: int = None, data: dict = None) -> Optional[dict]:
        url = f"{self.api_url}/{task_id}" if task_id else self.api_url
        method = {
            "get_all": "GET",
            "create": "POST",
            "update": "PUT",
            "delete": "DELETE"
        }.get(action, "GET")
        
        if action == "get_all":
            result = await self._make_request(method, self.api_url)
            return result if result else []
        elif action in ["create", "update"]:
            result = await self._make_request(method, url, data=data)
            return result
        elif action == "delete":
            await self._make_request(method, url)
            return None

    async def get_all(self) -> List[Task]:
        tasks = await self.perform_action("get_all")
        return [Task(**task) for task in tasks]

    async def create(self, title: str, status: str = "todo", solution: str = "") -> Optional[Task]:
        data = {"title": title, "status": status, "solution": solution}
        result = await self.perform_action("create", data=data)
        return Task(**result) if result else None

    async def update(self, task_id: int, title: Optional[str] = None, status: Optional[str] = None, solution: Optional[str] = None) -> Optional[Task]:
        task = await self.perform_action("get_all")
        task = next((t for t in task if t["id"] == task_id), None)
        if not task:
            return None
        data = {"title": title or task["title"], "status": status or task["status"], "solution": solution or task["solution"]}
        result = await self.perform_action("update", task_id, data)
        return Task(**result) if result else None

    async def delete(self, task_id: int):
        await self.perform_action("delete", task_id)