import os
import requests
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

app = FastAPI()


class BaseHTTPClient(ABC):
    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.default_headers = headers

    def _send_request(self, method: str, endpoint: str = "",
                      json_data: dict = None, headers: dict = None):
        url = f"{self.base_url}{endpoint}"
        headers = headers or self.default_headers

        response = requests.request(
            method=method,
            url=url,
            json=json_data,
            headers=headers
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Request failed: {response.text}"
            )
        return response.json()

    @abstractmethod
    def get(self, endpoint: str):
        pass

    @abstractmethod
    def post(self, endpoint: str, data: dict):
        pass

    @abstractmethod
    def put(self, endpoint: str, data: dict):
        pass

    @abstractmethod
    def delete(self, endpoint: str):
        pass


class JSONBinClient(BaseHTTPClient):
    def __init__(self):
        api_key = os.getenv("API_KEY")
        base_url = 'https://api.jsonbin.io/v3/b/'
        headers = {
            'Content-Type': 'application/json',
            'X-Master-Key': api_key
        }
        super().__init__(base_url, headers)

    def get(self, task_id: str):
        return self._send_request("GET", task_id)

    def post(self, data: dict):
        return self._send_request("POST", json_data=data)

    def put(self, task_id: str, data: dict):
        return self._send_request("PUT", task_id, json_data=data)

    def delete(self, task_id: str):
        return self._send_request("DELETE", task_id)


class LLMClient(BaseHTTPClient):
    def __init__(self):
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"
        headers = {
            "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_TOKEN')}"
        }
        super().__init__(base_url, headers)
        self.model = "@cf/meta/llama-3-8b-instruct"

    def get(self, endpoint: str):
        raise NotImplementedError("GET method not supported for LLMClient")

    def post(self, task_text: str):
        inputs = [
            {"role": "system", "content": "Ты — дружелюбный помощник, который объясняет, как решать задачи."},
            {"role": "user", "content": f"Объясни, как решить задачу: {task_text}"}
        ]
        input_payload = {"messages": inputs}
        response = self._send_request("POST",
                                      self.model, json_data=input_payload)
        return response["result"]["response"]

    def put(self, endpoint: str, data: dict):
        raise NotImplementedError("PUT method not supported for LLMClient")

    def delete(self, endpoint: str):
        raise NotImplementedError("DELETE method not supported for LLMClient")


class Task(BaseModel):
    title: str
    status: str


json_bin_client = JSONBinClient()
llm_client = LLMClient()


# id таски для примера 67f554708960c979a580c3fb
# id таски для примера 67f554518561e97a50fb31fd
@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    return json_bin_client.get(task_id)


@app.post("/tasks")
def create_task(task: Task):
    try:
        explanation = llm_client.post(task.title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

    data = {
        "title": task.title,
        "status": task.status,
        "explanation": explanation
    }
    return json_bin_client.post(data)


@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: Task):
    data = {
        "title": task.title,
        "status": task.status
    }
    return json_bin_client.put(task_id, data)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    return json_bin_client.delete(task_id)
