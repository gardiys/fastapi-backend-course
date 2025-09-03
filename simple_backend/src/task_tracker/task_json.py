import os
from dotenv import load_dotenv
import requests
from task import Task, TaskUpdate
from typing import List, Dict, Optional

load_dotenv()


class TasksJsonbin:

    def __init__(self, api_key: Optional[str] = None, bin_id: Optional[str] = None):
        self.__api_key = api_key or os.getenv('JSONBIN_API_KEY')
        self.__bin_id = bin_id or os.getenv('JSONBIN_BIN_ID')

        if not self.__api_key:
            raise ValueError(
                "Требуется ключ API. Укажите JSONBIN_API_KEY в env-файле или передайте в качестве аргумента"
            )

        self.headers = {
            'Content-Type': 'application/json',
            'X-Master-Key': self.__api_key,
            'X-Access-Key': self.__api_key
        }

        if self.__bin_id:
            self.url = f"https://api.jsonbin.io/v3/b/{self.__bin_id}"
        else:
            # Создаем новый bin автоматически
            self.url = self._create_new_bin()
            # Сохраняем ID newly created bin для возможного дальнейшего использования
            self.__bin_id = self.url.split('/')[-1]

    def _create_new_bin(self):
        try:
            response = requests.post(
                'https://api.jsonbin.io/v3/b',
                json={'tasks': []},
                headers=self.headers
            )
            response.raise_for_status()
            bin_data = response.json()
            bin_id = bin_data['metadata']['id']
            print(f"Создан новый bin с ID: {bin_id}")
            # Перезаписываем .env файл для сохранения JSONBIN_BIN_ID
            return f"https://api.jsonbin.io/v3/b/{bin_id}"
        except Exception as error:
            raise print(f"Ошибка при создании bin: {error}")

    def _read_data(self) -> Dict:
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
        return [Task(**dct) for dct in self._read_data()['tasks']]

    def add(self, task: Task):
        tasks = self._read_data()
        task_add = tasks.get('tasks')
        task_add.append(task.__dict__)
        tasks['tasks'] = task_add
        self._write_data(tasks)
        return 'ok'

    def up_data(self, task_id: str, task: TaskUpdate):
        tasks = self._read_data()
        dct = self._search_task(task_id, tasks['tasks'])
        dct_up = {key: value for key, value in task.__dict__.items() if value != None}
        dct.update(dct_up)
        self._write_data(tasks)
        return 'ok'

    def delete(self, task_id: str):
        tasks = self._read_data()
        dct = self._search_task(task_id, tasks['tasks'])
        tasks['tasks'].pop(tasks['tasks'].index(dct))
        self._write_data(tasks)
        return 'ok'
