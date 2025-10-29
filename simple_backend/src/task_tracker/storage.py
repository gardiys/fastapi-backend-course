import json
import os

class FileStorage:
    def __init__(self, filename='tasks.json'):
        self.json_name = filename
    
    def load_tasks(self):
        if not os.path.exists(self.json_name):
            return []
        
        try:
            with open(self.json_name, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self, task_list):
        with open(self.json_name, 'w', encoding='utf-8') as file:
            json.dump(task_list, file)