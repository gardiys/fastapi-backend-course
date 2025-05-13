import json
import os
from typing import List
from main import Task

class TaskStorage:
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    def load_tasks(self) -> List[Task]:
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Task(**item) for item in data]
        
    def save_tasks(self, tasks: List[Task]):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([task.dict() for task in tasks], f, indent=2, ensure_ascii=False)