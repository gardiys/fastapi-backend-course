from dataclasses import dataclass
from typing import List, Optional, Dict
from pydantic import BaseModel
from base_http_client import BaseHTTPClient

class Task(BaseModel):
    id: Optional[str] = None
    title: str
    status: str = "to do"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None


@dataclass
class MockApiConfig:
    api_url: str
    resource: str = "tasks"


class MockApiTasks(BaseHTTPClient):
    def __init__(self, cfg: MockApiConfig):
        self._cfg = cfg
        super().__init__(api_url=cfg.api_url, default_timeout=20.0)

    def _default_headers(self) -> Dict[str, str]:
        return {}

    def _collections_url(self) -> str:
        return self._cfg.resource
    
    def _item_url(self, task_id: str) -> str:
        return f"{self._collections_url()}/{task_id}"
    
    def get_all(self) -> List[Task]:
        response = self.get(self._collections_url())
        response.raise_for_status()
        data = response.json()
        return [Task(**task) for task in data]
    
    def get_by_id(self, task_id: str) -> Task:
        response = self.get(self._item_url(task_id))
        if response.status_code == 404:
            raise KeyError("Task not found")
        response.raise_for_status()
        return Task(**response.json())

    def add(self, task_in: Task) -> Task:
        payload = task_in.model_dump(exclude={"id"})
        response = self.post(self._collections_url(), json=payload)
        response.raise_for_status()
        return Task(**response.json())
    
    def update(self, task_id: str, task_update: TaskUpdate) -> Task:
        payload = task_update.model_dump(exclude_none=True)
        if not payload:
            return self.get_by_id(task_id)
        
        response = self.put(self._item_url(task_id), json=payload)
        if response.status_code == 404:
            raise KeyError("Task not found")
        response.raise_for_status()
        return Task(**response.json())
    
    def delete(self, task_id: str) -> None:
        response = self.delete(self._item_url(task_id))
        if response.status_code == 404:
            raise KeyError("Task not found")
        response.raise_for_status()