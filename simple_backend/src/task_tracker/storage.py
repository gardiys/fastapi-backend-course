import json
import os
from typing import List, Dict, Any
from base_client import BaseHTTPClient

class FileStorage:
    
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file

    def load_tasks(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_tasks(self, tasks: List[Dict[str, Any]]) -> bool:
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка сохранения в файл: {e}")
            return False

class FileStorageAdapter(BaseHTTPClient):
    
    def __init__(self, data_file: str = "tasks.json"):
        super().__init__("file://localhost")
        self.storage = FileStorage(data_file)

    def load_tasks(self):
        return self.storage.load_tasks()

    def save_tasks(self, tasks):
        return self.storage.save_tasks(tasks)