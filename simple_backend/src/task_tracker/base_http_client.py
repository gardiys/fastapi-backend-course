from abc import ABC, abstractmethod
import requests

class BaseHTTPClient(ABC):
    def __init__(self, token: str, url: str):
        self.token = token
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get(self):
        """Общий GET-запрос"""
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print("HTTP GET Error:", e)
            raise

    def post(self, payload: dict):
        """Общий POST-запрос"""
        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print("HTTP POST Error:", e)
            raise

    def patch(self, payload: dict):
        """Общий PATCH-запрос"""
        try:
            response = requests.patch(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print("HTTP PATCH Error:", e)
            raise

    @abstractmethod
    def load_data(self):
        """Обязательный метод для наследников"""
        pass

    @abstractmethod
    def save_data(self, data):
        """Обязательный метод для наследников"""
        pass

