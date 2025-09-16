import requests
import json

class CloudStorage:
    def __init__(self, api_url: str, api_key: str = None):
        self.api_url = api_url
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["X-API-Key"] = api_key
    
    def get_all_tasks(self):
        response = requests.get(self.api_url, headers=self.headers)
        return response.json()
    
    def create_task(self, task_name, task_status):
        tasks = self.get_all_tasks()
        
        if tasks:
            task_id = max(task['id'] for task in tasks) + 1
        else:
            task_id = 1
        
        new_task = {'id': task_id, 'name': task_name, 'status': task_status}
        tasks.append(new_task)
        
        response = requests.put(self.api_url, json=tasks, headers=self.headers)
        return new_task
    
    def update_task(self, task_id, new_name, new_status):
        tasks = self.get_all_tasks()
        
        for task in tasks:
            if task['id'] == task_id:
                task['name'] = new_name
                task['status'] = new_status
                response = requests.put(self.api_url, json=tasks, headers=self.headers)
                return task
        
        return None
    
    def delete_task(self, task_id):
        tasks = self.get_all_tasks()
        
        for i, task in enumerate(tasks):
            if task['id'] == task_id:
                deleted_task = tasks.pop(i)
                response = requests.put(self.api_url, json=tasks, headers=self.headers)
                return deleted_task
        
        return None