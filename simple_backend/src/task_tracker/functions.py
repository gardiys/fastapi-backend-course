import json
from typing import Dict, List

import httpx
import requests


class TaskTracker:
    def __init__(self, filename: str):
        self.filename = filename

    def load_tasks(self) -> List[Dict]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_tasks(self, tasks: List[Dict]):
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(tasks, file, ensure_ascii=False, indent=4)
                return 'данные сохранены'
        except IOError:
            return 'ошибка при записи файла'

    def get_all_tasks(self) -> List[Dict]:
        return self.load_tasks()

    def add_task(self, task: Dict) -> str:
        tasks = self.load_tasks()
        for existing_task in tasks:
            if existing_task['id'] == task['id']:
                return 'задача уже существует'
        tasks.append(task)
        self.save_tasks(tasks)
        return 'задача добавлена'

    def update_task(self, task_id: int, name: str, status: str) -> str:
        tasks = self.load_tasks()
        for task in tasks:
            if task['id'] == task_id:
                task['name'] = name
                task['status'] = status
                self.save_tasks(tasks)
                return 'задача обновлена'
        return 'task not found'

    def delete_task(self, task_id: int):
        tasks = self.load_tasks()
        for task in tasks:
            if task['id'] == task_id:
                tasks.remove(task)
                self.save_tasks(tasks)
                return 'задача удалена'
        return 'task not found'


class TaskTrackerCloud:
    def __init__(self, api_key, bin_id=None):
        self.api_key = api_key
        self.bin_id = bin_id
        self.base_url = "https://api.jsonbin.io/v3/b"

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "X-Master-Key": self.api_key,
            "X-Bin-Private": "true"
        }

    def load_tasks(self):
        if not self.bin_id:
            return []

        url = f"{self.base_url}/{self.bin_id}"
        response = requests.get(url, headers=self._get_headers())

        if response.status_code == 200:
            return response.json().get('record', [])
        return []

    def save_tasks(self, tasks):
        data = json.dumps(tasks, ensure_ascii=False)
        headers = self._get_headers()

        if self.bin_id:
            url = f"{self.base_url}/{self.bin_id}"
            response = requests.put(url, headers=headers, data=data)
        else:
            url = self.base_url
            headers["X-Collection-Id"] = ""
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                self.bin_id = response.json().get('metadata', {}).get('id')

        return response.status_code in (200, 201)

    def get_all_tasks(self):
        return self.load_tasks()

    def add_task(self, task):
        tasks = self.load_tasks()
        for existing_task in tasks:
            if existing_task['id'] == task['id']:
                return 'задача уже существует'
        tasks.append(task)
        if self.save_tasks(tasks):
            return 'задача добавлена'
        return 'ошибка при сохранении'

    def update_task(self, task_id, name, status):
        tasks = self.load_tasks()
        for task in tasks:
            if task['id'] == task_id:
                task['name'] = name
                task['status'] = status
                if self.save_tasks(tasks):
                    return 'задача обновлена'
                return 'ошибка при сохранении'
        return 'task not found'

    def delete_task(self, task_id):
        tasks = self.load_tasks()
        for task in tasks:
            if task['id'] == task_id:
                tasks.remove(task)
                if self.save_tasks(tasks):
                    return 'задача удалена'
                return 'ошибка при сохранении'
        return 'task not found'