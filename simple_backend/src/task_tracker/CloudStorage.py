import requests
from typing import List
from models import Task
from base_client import BaseHTTPClient

class CloudStorage(BaseHTTPClient):
    def __init__(self, bin_url: str, api_key: str):
        print("🔧 CloudStorage инициализируется с URL:", bin_url)
        headers = {
            "X-Master-Key": api_key,
            "Content-Type": "application/json"
        }
        super().__init__(bin_url, headers)
        
    def load_tasks(self) -> List[Task]:
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        
        data = response.json()
        raw = data.get("record")
        if not isinstance(raw, list):
            return []
        
        migrated_tasks = []
        
        for item in raw:
            #title->description миграция
            if "title" in item and "description" not in item:
                item["description"] = item.pop("title")
                
            if "solution" not in item:
                item["solution"] = None
                
            try:
                migrated_tasks.append(Task(**item))
            except Exception as e:
                print("Ошибка при создании Task:", e)
                continue
            
        if migrated_tasks and migrated_tasks != raw:
            self.save_tasks(migrated_tasks)

        return migrated_tasks
    
    def save_tasks(self, tasks: List[Task]):
        response = requests.put(self.url, headers=self.headers, json=[task.dict() for task in tasks])
        response.raise_for_status()
        
    def _required_method(self):
        pass