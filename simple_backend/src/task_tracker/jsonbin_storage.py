import requests

class JSONBinStorage:
    def __init__(self, bin_id: str, api_key: str):
        self.bin_id = bin_id
        self.api_key = api_key
        self.url = f"https://api.jsonbin.io/v3/b/{self.bin_id}"

    def _headers(self):
        return {
            "X-Master-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def get_tasks(self):
        r = requests.get(self.url, headers=self._headers())
        r.raise_for_status()
        return r.json()['record']

    def update_tasks(self, tasks):
        r = requests.put(self.url, json=tasks, headers=self._headers())
        r.raise_for_status()
        return r.json()['record']

    def create_task(self, task):
        tasks = self.get_tasks()
        tasks.append(task)
        return self.update_tasks(tasks)

    def update_task(self, task_id, updated_task):
        tasks = self.get_tasks()
        for i, task in enumerate(tasks):
            if task.get("id") == task_id:
                tasks[i] = updated_task
                return self.update_tasks(tasks)
        raise ValueError("Task not found")

    def delete_task(self, task_id):
        tasks = self.get_tasks()
        for i, task in enumerate(tasks):
            if task.get("id") == task_id:
                tasks.pop(i)
                return self.update_tasks(tasks)
        raise ValueError("Task not found")

