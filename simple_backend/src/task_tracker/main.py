from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests

app = FastAPI()

JSON_API_KEY = os.getenv('JSONBIN_API_KEY')
JSON_BIN_ID = '67d51a948a456b7966761e9c'
JSON_HEADERS = {
  'Content-Type': 'application/json',
  'X-Master-Key': JSON_API_KEY
}

CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/ai/llm"
CLOUDFLARE_API_KEY = os.getenv('CLOUDFLARE_API_KEY')
CLOUDFLARE_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CLOUDFLARE_API_KEY}"
}


class Task(BaseModel):
    name: str
    status: str
    solution: str = ''

    def __repr__(self):
        return f"Task(name={self.name}, status={self.status})"


class CloudFlareLLM:
    @staticmethod
    def get_solution(task_name):
        ask = {'prompt': f'Объясни, как решить следующую задачу: {task_name}'}
        try:
            response = requests.post(CLOUDFLARE_API_URL, headers=CLOUDFLARE_HEADERS, json=ask)
            response.raise_for_status()
            data = response.json()
            return data.get('solution', 'Не удалось получить решение')
        except requests.RequestException as err:
            return {'error': str(err)}


class TaskTracker:
    def __init__(self, bin_id):
        self.url = f'https://api.jsonbin.io/v3/b/{bin_id}'
        self.bin_id = bin_id

    def read_json(self):
        try:
            response = requests.get(self.url, headers=JSON_HEADERS)
            response.raise_for_status()
            data = response.json()
            return data.get('record', {})
        except requests.RequestException as err:
            return {'error': str(err)}

    def _write_json(self, info):
        try:
            response = requests.put(self.url, json={"record": info}, headers=JSON_HEADERS)
            response.raise_for_status()
            return {'message': 'Данные обновлены'}
        except requests.RequestException as err:
            return {'error': str(err)}

    def add_json(self, task):
        info = self.read_json()
        task_id = max(map(int, info.keys()), default=0) + 1
        task.solution = CloudFlareLLM.get_solution(task.name)
        info[str(task_id)] = task.dict()
        return self._write_json(info)

    def delete_json(self, task_id: int):
        info = self.read_json()
        if str(task_id) not in info:
            raise HTTPException(status_code=404, detail='task not found')
        del info[str(task_id)]
        return self._write_json(info)

    def update_json(self, task_id, task):
        info = self.read_json()
        if str(task_id) not in info:
            raise HTTPException(status_code=404, detail='task not found')
        info[str(task_id)] = task.dict()
        return self._write_json(info)


tracker = TaskTracker(JSON_BIN_ID)


@app.get("/tasks")
def get_tasks():
    return tracker.read_json()


@app.post("/tasks")
def create_task(task: Task):
    return tracker.add_json(task)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    return tracker.update_json(task_id, task)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return tracker.delete_json(task_id)

