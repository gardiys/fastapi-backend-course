from abc import abstractmethod
import requests
from model import Task


class BaseHTTPClient:
    def __init__(self, base_url: str, timeout: int):
        self.base_url = base_url
        self.timeout = timeout

    def get(self, url: str) -> dict:
        response = requests.get(f"{self.base_url}{url}", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def post(self, url: str, data: dict, headers: dict = None) -> dict:
        if headers:
            response = requests.post(
                f"{self.base_url}{url}",
                json=data,
                timeout=self.timeout,
                headers=headers,
            )
        else:
            response = requests.post(
                f"{self.base_url}{url}", json=data, timeout=self.timeout
            )
        response.raise_for_status()
        return response.json()

    def put(self, url: str, data: dict) -> dict:
        response = requests.put(
            f"{self.base_url}{url}", json=data, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def delete(self, url: str) -> dict:
        response = requests.delete(f"{self.base_url}{url}", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    @abstractmethod
    def json_to_task(self, data: dict | list[dict]) -> Task | list[Task]:
        pass
