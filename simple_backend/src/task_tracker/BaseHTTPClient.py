import requests
from abc import ABC, abstractmethod

class BaseHTTPClient(ABC):

    def __init__(self, base_url: str, headers: dict = None):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}

    def _get(self, endpoint: str = "", **kwargs):
        url = f"{self.base_url}{endpoint}"
        print(f"[GET] {url}")
        resp = requests.get(url, headers=self.headers, timeout=15, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def _post(self, endpoint: str = "", json_data=None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        print(f"[POST] {url} | DATA: {json_data}")
        resp = requests.post(url, headers=self.headers, json=json_data, timeout=15, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def _patch(self, endpoint: str = "", json_data=None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        print(f"[PATCH] {url} | DATA: {json_data}")
        resp = requests.patch(url, headers=self.headers, json=json_data, timeout=15, **kwargs)
        resp.raise_for_status()
        return resp.json()

    @abstractmethod
    def _make_request(self, *args, **kwargs):
        pass
        