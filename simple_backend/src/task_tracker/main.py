from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests
from abc import ABC, abstractmethod

app = FastAPI()

JSON_API_KEY = os.getenv('JSONBIN_API_KEY')
JSON_BIN_ID = '67d51a948a456b7966761e9c'
JSON_HEADERS = {
  'Content-Type': 'application/json',
  'X-Master-Key': JSON_API_KEY
}

CLOUDFLARE_API_KEY = os.getenv('CLOUDFLARE_API_KEY')
CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/ai/llm"
CLOUDFLARE_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CLOUDFLARE_API_KEY}"
}

if not JSON_API_KEY or not CLOUDFLARE_API_KEY:
    raise ValueError('API-ключ не найден. Убедитесь, что он указан в .env')

class Task(BaseModel):
    name: str
    status: str
    solution: str = ''

    def __repr__(self):
        return f"Task(name={self.name}, status={self.status})"


class BaseHTTPClient(ABC):
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def get(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as err:
            return {"error": str(err)}

    def put(self, data):
        try:
            response = requests.put(self.url, json=data, headers=self.headers)
            response.raise_for_status()
            return {"message": "Данные обновлены"}
        except requests.RequestException as err:
            return {"error": str(err)}

    @abstractmethod
    def process_response(self, response):
        pass

class CloudFlareLLM(BaseHTTPClient):
    def __init__(self):
        super().__init__(CLOUDFLARE_API_URL, CLOUDFLARE_HEADERS)

    def get_solution(self, task_name):
        ask = {"prompt": f"Объясни, как решить следующую задачу: {task_name}"}
        try:
            response = requests.post(self.url, headers=self.headers, json=ask)
            response.raise_for_status()
            return self.process_response(response)
        except requests.RequestException as err:
            return {"error": str(err)}

    def process_response(self, response):
        data = response.json()
        return data.get("solution", "Не удалось получить решение")


class TaskTracker(BaseHTTPClient):
    def __init__(self, bin_id):
        super().__init__(f"https://api.jsonbin.io/v3/b/{bin_id}", JSON_HEADERS)
        self.bin_id = bin_id

    def read_json(self):
        response = self.get()
        return response.get("record", {})

    def write_json(self, info):
        return self.put({"record": info})

    def process_response(self, response):
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as err:
            return {"error": str(err)}

    def add_json(self, task):
        info = self.read_json()
        task_id = max(map(int, info.keys()), default=0) + 1
        task.solution = CloudFlareLLM().get_solution(task.name)
        info[str(task_id)] = task.dict()
        return self.write_json(info)

    def delete_json(self, task_id: int):
        info = self.read_json()
        if str(task_id) not in info:
            raise HTTPException(status_code=404, detail="task not found")
        del info[str(task_id)]
        return self.write_json(info)

    def update_json(self, task_id, task):
        info = self.read_json()
        if str(task_id) not in info:
            raise HTTPException(status_code=404, detail="Task not found")
        info[str(task_id)] = task.dict()
        return self.write_json(info)


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

