from abc import ABC, abstractmethod
import requests

class BaseHTTPClient(ABC):
    def __init__(self, base_url: str, headers: dict):
        self.url = base_url
        self.headers = headers

    def get(self):
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def put(self, data):
        response = requests.put(self.url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, data):
        response = requests.post(self.url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    @abstractmethod
    def handle(self, *args, **kwargs):
        pass