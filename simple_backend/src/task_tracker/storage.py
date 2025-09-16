import json
import os
from pathlib import Path

class FileStorage:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def _read_tasks(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def _write_tasks(self, tasks_data):
        with open(self.file_path, 'w') as f:
            json.dump(tasks_data, f, indent=2)
    
    def get_all_tasks(self):
        return self._read_tasks()
    
    def create_task(self, task_name, task_status):
        tasks_data = self._read_tasks()
        
        if tasks_data:
            task_id = max(task['id'] for task in tasks_data) + 1
        else:
            task_id = 1
        
        new_task = {'id': task_id, 'name': task_name, 'status': task_status}
        tasks_data.append(new_task)
        self._write_tasks(tasks_data)
        return new_task
    
    def update_task(self, task_id, new_name, new_status):
        tasks_data = self._read_tasks()
        
        for task in tasks_data:
            if task['id'] == task_id:
                task['name'] = new_name
                task['status'] = new_status
                self._write_tasks(tasks_data)
                return task
        
        return None
    
    def delete_task(self, task_id):
        tasks_data = self._read_tasks()
        
        for i, task in enumerate(tasks_data):
            if task['id'] == task_id:
                deleted_task = tasks_data.pop(i)
                self._write_tasks(tasks_data)
                return deleted_task
        
        return None