import json
from pathlib import Path
from tkinter import NO

class TaskStorage():
    def __init__(self, filename='tasks.json'):
        self.filepath = Path(filename)
        if not self.filepath.exists():
            self._save([])
            
    def _load(self):
        with open(self.filepath, 'r', encoding='utf8') as file:
            return json.load(file)
        
    def _save(self, tasks):
        with open(self.filepath, 'w', encoding='utf8') as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)
    
    def get_tasks(self):
        self._load()
        
    def add_task(self, task):
        tasks = self._load()
        task['id'] = self._generate_id(tasks)
        task.setdefault('status', 'panding')
        tasks.append(task)
        self._save(tasks)
        return task        
            
    def update_task(self, task_id, new_data):
        tasks = self._load()
        for task in tasks:
            if task['id'] == task_id:
                task.update(new_data)
                self._save(tasks)
                return task
        return None
    
    def delete_task(self, task_id):
        tasks = self._load()
        updated = [task for task in tasks if task['id'] != task_id]
        if len(tasks) == len(updated):
            return False
        self._save(updated)
        return True
    
    def _generate_id(self, tasks):
        if not tasks:
            return 1
        return max(task['id'] for task in tasks) + 1    