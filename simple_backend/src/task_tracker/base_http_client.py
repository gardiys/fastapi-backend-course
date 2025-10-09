from abc import ABC
from typing import Any
import requests

class BaseHTTPClient(ABC):
    def __init__(self, token: str, url: str):
        self.token = token
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get(self) -> dict[str, Any]:
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(self.url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def patch(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.patch(self.url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
