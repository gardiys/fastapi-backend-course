from abc import ABC, abstractmethod
import requests

class BaseHTTPClient(ABC):
    def __init__(self, url: str, headers: dict = None):
        self.url = url
        self.headers = headers or {}
        
    def get(self, path: str = ""):
        response = requests.get(f"{self.url}{path}", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def post(self, data: dict, path: str = ""):
        response = requests.post(f"{self.url}{path}", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def put(self, data: dict, path: str = ""):
        response = requests.put(f"{self.url}{path}", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    @abstractmethod
    def _required_method(self):
        pass