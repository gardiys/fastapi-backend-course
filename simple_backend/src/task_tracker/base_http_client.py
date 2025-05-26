from abc import ABC, abstractmethod
import requests

class BaseHTTPClient(ABC):
    def __init__(self, base_url: str, headers: dict = None):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}

    def _get(self, endpoint: str = "", **kwargs):
        return self._request("get", endpoint, **kwargs)

    def _post(self, endpoint: str = "", json=None, **kwargs):
        return self._request("post", endpoint, json=json, **kwargs)

    def _put(self, endpoint: str = "", json=None, **kwargs):
        return self._request("put", endpoint, json=json, **kwargs)

    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        return response.json()

    @abstractmethod
    def perform_action(self, *args, **kwargs):
        pass
