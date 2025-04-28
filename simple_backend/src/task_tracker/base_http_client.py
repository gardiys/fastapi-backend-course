from abc import ABC, abstractmethod
import requests


class BaseHTTPClient(ABC):
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def get(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as err:
            return {"error": str(err)}

    def put(self, data):
        try:
            response = requests.put(self.url, json=data, headers=self.headers)
            response.raise_for_status()
            return {"message": "Данные обновлены"}
        except requests.RequestException as err:
            return {"error": str(err)}

    @abstractmethod
    def process_response(self, response):
        pass