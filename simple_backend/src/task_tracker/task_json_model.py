import requests
from task_model import Task
from abc_model import BaseHTTPClient
from typing import List, Dict


class TasksJsonbin(BaseHTTPClient):

    def __init__(self, api_key: str, bin_id: str):
        self.url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Master-Key': api_key,
            'X-Access-Key': api_key
        }

    def request(self) -> Dict:
        response = requests.get(url=self.url, headers=self.headers)
        response.raise_for_status()
        return response.json()['record']

    def _write_data(self, data: Dict):
        response = requests.put(self.url, json=data, headers=self.headers)
        response.raise_for_status()
        return 'Ok'

    def _search_task(self, task_id: str, tasks: Dict) -> Dict:
        for dct in tasks:
            if task_id == dct.get("id"):
                return dct
        raise KeyError(f"Задача с task_id {task_id} не найдена")

    def get_all_tasks(self) -> List:
        return [Task(**dct) for dct in self.request()['tasks']]

    def add(self, task: Task):
        tasks = self.request()
        task_add = tasks.get('tasks')
        task_add.append(task.__dict__)
        tasks['tasks'] = task_add
        self._write_data(tasks)
        return 'ok'

    def up_data(self, task_id: str, dct_up: Dict):
        tasks = self.request()
        dct = self._search_task(task_id, tasks['tasks'])
        dct.update(dct_up)
        self._write_data(tasks)
        return 'ok'

    def delete(self, task_id: str):
        tasks = self.request()
        dct = self._search_task(task_id, tasks['tasks'])
        tasks['tasks'].pop(tasks['tasks'].index(dct))
        self._write_data(tasks)
        return 'ok'
