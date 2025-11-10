import requests

class BaseHTTPClient:
    def __init__(self, base_url: str, headers: dict | None = None):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}

    def get(self, endpoint: str = "", **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        res = requests.get(url, headers=self.headers, **kwargs)
        res.raise_for_status()
        return res.json()

    def post(self, endpoint: str = "", json: dict | None = None, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        res = requests.post(url, headers=self.headers, json=json, **kwargs)
        res.raise_for_status()
        return res.json()

    def put(self, endpoint: str = "", json: dict | None = None, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        res = requests.put(url, headers=self.headers, json=json, **kwargs)
        res.raise_for_status()
        return res.json()


