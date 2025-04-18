from abc import ABC, abstractmethod
import requests


class BaseHTTPClient(ABC):
    def __init__(self, base_url: str, headers: dict[str, str] | None = None):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}

    @abstractmethod
    def parse_response(self, response: requests.Response):
        pass

    def _request(self, method: str, json: dict | None = None):
        try:
            response = requests.request(
                method=method,
                url=self.base_url,
                headers=self.headers,
                json=json,
                timeout=15,
            )

            response.raise_for_status()
            return self.parse_response(response)
        except requests.RequestException as exc:
            print(f"[HTTP Error] {method} {self.base_url}: {exc}")
            return None
