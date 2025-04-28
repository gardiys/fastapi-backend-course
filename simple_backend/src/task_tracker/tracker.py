from fastapi import HTTPException
from pydantic import BaseModel
import os
import requests
from cloudflare_llm import CloudFlareLLM
from base_http_client import BaseHTTPClient
from dotenv import load_dotenv

load_dotenv()

JSON_API_KEY = os.getenv('JSONBIN_API_KEY')
JSON_BIN_ID = '67d51a948a456b7966761e9c'
JSON_HEADERS = {
  'Content-Type': 'application/json',
  'X-Master-Key': JSON_API_KEY
}

if not JSON_API_KEY:
    raise ValueError('API-ключ не найден. Убедитесь, что он указан в .env')

class Task(BaseModel):
    name: str
    status: str
    solution: str = ''

    def __repr__(self):
        return f"Task(name={self.name}, status={self.status})"


class TaskTracker(BaseHTTPClient):
    def __init__(self):
        super().__init__(f"https://api.jsonbin.io/v3/b/{JSON_BIN_ID}", JSON_HEADERS)

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