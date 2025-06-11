import requests
import os
from http_client import BaseHTTPClient
from typing import Any


class JsonBinStorage(BaseHTTPClient):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('JSONBIN_API_KEY')
        self.bin_id = os.getenv('JSONBIN_BIN_ID')
        self.base_url = "https://api.jsonbin.io/v3/b"
        self.headers = {
            "Content-Type": "application/json",
            "X-Master-Key": self.api_key,
            "x-Bin-Versioning": "false"
        }

    def _prepare_request_data(self, tasks: Any) -> dict[str, Any]:
        return tasks if tasks else []

    def _process_response(self, response_data: dict[str, Any]) -> list[Any]:
        return response_data.get("record", [])

    def read_tasks(self) -> list:
        response = self._make_request("GET", f"/{self.bin_id}/latest")
        return self._process_response(response) if response else []

    def save_task(self, tasks: list) -> bool:
        response = self._make_request(
            "PUT", f"/{self.bin_id}", self._prepare_request_data(tasks))
        return response is not None
    
    def get_next_id(self, tasks: list[dict[str, Any]]) -> int:
        """Генерация следующего ID"""
        return max((task.get("id", 0) for task in tasks), default=0) + 1
