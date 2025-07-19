import json
from base_http_client import BaseHTTPClient


class CloudStorage(BaseHTTPClient):
    def __init__(self, bin_id: str, api_key: str):
        super().__init__(
            base_url=f'https://api.jsonbin.io/v3/b/{bin_id}',
            headers={
                'X-Master-Key': api_key,
                'Content-Type': 'application/json'
            }
        )

    def _parse_response(self, response):
        try:
            record = response.json().get("record", {})
            
            if isinstance(record, str):
                try:
                    record = json.loads(record)
                except json.JSONDecodeError:
                    record = {"tasks": []}
            
            if isinstance(record, dict) and "tasks" not in record:
                record = {"tasks": [record]} if record else {"tasks": []}
                
            return record
        except Exception as e:
            print(f"Error parsing response: {e}")
            return {"tasks": []}

    def get_tasks(self) -> list[dict]:
        response = self.send_request("GET")
        data = self._parse_response(response)
        if isinstance(data, dict):
            return data.get("tasks", [])
        elif isinstance(data, list):
            return data
        return [] 

    def _save(self, tasks: list[dict]):
        data = {"tasks": tasks} if not isinstance(tasks, dict) else tasks
        response = self.send_request("PUT", json=data)
        if response.status_code != 200:
            raise Exception("Ошибка при сохранении задач")

    def add_task(self, task: dict) -> dict:
        tasks = self.get_tasks()
        if not isinstance(tasks, list):
            tasks = []
        
        task["id"] = self._generate_id(tasks)
        task.setdefault("status", "pending")
        
        tasks.append(task)
        self._save(tasks)
        return task

    def update_task(self, task_id: int, new_data: dict) -> dict | None:
        tasks = self.get_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task.update(new_data)
                self._save(tasks)
                return task
        return None

    def delete_task(self, task_id: int) -> bool:
        tasks = self.get_tasks()
        updated = [task for task in tasks if task["id"] != task_id]
        if len(updated) == len(tasks):
            return False
        self._save(updated)
        return True

    def _generate_id(self, tasks: list[dict]) -> int:
        if not tasks:
            return 1
        try:
            return max(int(task.get("id", 0)) for task in tasks if isinstance(task, dict)) + 1
        except (ValueError, TypeError):
            return 1
