from abc import ABC, abstractmethod
import requests

class BaseHTTPClient(ABC):
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    @abstractmethod
    def _get_auth_headers(self) -> dict:
        pass

    def _post(self, endpoint: str = "", json: dict = None):
        url = f"{self.base_url}/{endpoint}".rstrip("/")
        headers = self._get_auth_headers()
        response = requests.post(url, headers=headers, json=json)
        response.raise_for_status()
        return response.json()
