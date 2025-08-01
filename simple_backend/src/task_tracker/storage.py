import requests
from typing import List
from pydantic import BaseModel

class RemoteTaskStorage:
    def __init__(self, bin_id: str, api_key: str):
        self.url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        self.headers = {
            "X-Master-Key": api_key,
            "Content-Type": "application/json"
        }

    def load(self) -> List[dict]:
        response = requests.get(self.url + "/latest", headers=self.headers)
        response.raise_for_status()
        return response.json()["record"]

    def save(self, tasks: List[dict]) -> None:
        response = requests.put(self.url, headers=self.headers, json=tasks)
        response.raise_for_status()
