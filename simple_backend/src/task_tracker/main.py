from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from dotenv import load_dotenv
from openai import OpenAI
from abc import ABC, abstractmethod
import json
import random
import requests
import os

class Status(Enum):
    OPEN = "OPEN"
    IN_PROCESS = "IN_PROCESS"
    ON_REVIEW = "ON_REVIEW"
    CLOSED = "CLOSED"
    
class Task(BaseModel):
    status: Status
    descr: str
    ai_solve_idea: str = ""


class BaseHTTPClient(ABC):
    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.headers = headers

    @abstractmethod
    def _send_request(self, method: str, endpoint: str, **kwargs):
        pass

    def get(self, endpoint: str, params: dict = None):
        return self._send_request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: dict = None):
        return self._send_request("POST", endpoint, json=json)

    def patch(self, endpoint: str, json: dict = None):
        return self._send_request("PATCH", endpoint, json=json)

class GistClient(BaseHTTPClient):
    def __init__(self, token: str):
        base_url = "https://api.github.com"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        super().__init__(base_url, headers)

    def _send_request(self, method: str, endpoint: str, **kwargs):
        response = requests.request(
            method,
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

class OpenRouterClient(BaseHTTPClient):
    def __init__(self, api_key: str, base_url: str):
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        super().__init__(base_url, headers)

    def _send_request(self, method: str, endpoint: str, **kwargs):
        response = requests.request(
            method,
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

    def create_chat_completion(self, model: str, messages: list):
        return self.post(
            "/chat/completions",
            json={"model": model, "messages": messages}
        )

class Storage:
    def __init__(self, client: GistClient, gist_id: str, filename: str):
        self.client = client
        self.gist_id = gist_id
        self.filename = filename

    def get_tasks_from_database(self):
        data = self.client.get(f"/gists/{self.gist_id}")
        return json.loads(data['files'][self.filename]['content'])

    def dump_tasks_to_database(self, tasks):
        self.client.patch(
            f"/gists/{self.gist_id}",
            json={"files": {self.filename: {"content": json.dumps(tasks)}}}
        )


app = FastAPI()
load_dotenv()

gist_client = GistClient(os.getenv('TOKEN'))
openrouter_client = OpenRouterClient(
    api_key = os.getenv('OPENROUTER_API_KEY'),
    base_url="https://openrouter.ai/api/v1"
)
storage = Storage(gist_client, os.getenv('GIST_ID'), os.getenv('GIST_FILENAME'))


@app.get("/tasks")
def get_tasks():
    return storage.get_tasks_from_database()
    

@app.post("/tasks")
def create_task(task:Task):
    
    task = task.model_dump(mode = "json")
    task_id = abs(hash(random.randbytes(32)))
    
    tasks = storage.get_tasks_from_database()

    
    completion = openrouter_client.create_chat_completion(
        model="deepseek/deepseek-r1:free",
        messages=[
            {
                "role": "system",
                "content": "You are an assistaint. User will send you task, and you must give user an advice about how to solve this task. Answer in russian."
            },
            {
                "role": "user",
                "content": task['descr']
            }
        ]
    )
    task['ai_solve_idea'] = completion['choices'][0]['message']['content']
    tasks[task_id] = task

    storage.dump_tasks_to_database(tasks)

    return f"Task created with id {task_id}"

@app.put("/tasks/{task_id}")
def update_task(task_id: int, new_status: Status):

    tasks = storage.get_tasks_from_database()
    try:
        tasks[str(task_id)]['status'] = new_status.value
    except KeyError:
        return "No task with this ID"
    
    storage.dump_tasks_to_database(tasks)
            
    return "Task status changed succesfully"

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = storage.get_tasks_from_database()
    try:
        tasks.pop(str(task_id))
    except KeyError:
        return "No task with this ID"
    storage.dump_tasks_to_database(tasks)
    return "Task deleted succesfully"
