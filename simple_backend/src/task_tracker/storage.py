import json
import os
class TaskStorage:
    def __init__(self, filename: str = 'tasks.json'):
        self.file = filename
        if not os.path.exists(self.file):  # if file does not exist, create file with empty list
            self.save([])
    def load(self):
        with open(self.file, 'r', encoding = 'utf-8') as f:
            return json.load(f)
    def save(self, tasks):
        with open(self.file, 'w', encoding = 'utf-8') as f:
            json.dump(tasks, f)