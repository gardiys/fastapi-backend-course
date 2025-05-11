import requests
from typing import List
from models import Task

class CloudStorage:
    def __init__(self, bin_url: str, api_key: str):
        self.url = bin_url
        self.headers = {
            "X-Master-Key": api_key,
            "Content-Type": "application/json"
        }
        
    def load_tasks(self) -> List[Task]:
        response = requests.get(self.url, headers=self.headers)
        
        print("RESPONSE STATUS:", response.status_code)
        try:
            print("RESPONSE JSON:", response.json())
        except Exception as e:
            print("Ошибка при получении JSON:", e)
        
        response.raise_for_status()
        
        data = response.json()
        raw = data.get("record")
        if not isinstance(raw, list):
            return []
        
        return [Task(**item) for item in raw]
    
    def save_tasks(self, tasks: List[Task]):
        response = requests.put(self.url, headers=self.headers, json=[task.dict() for task in tasks])
        response.raise_for_status()