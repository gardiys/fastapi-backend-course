from abc import ABC, abstractmethod
import requests


class BaseHTTPClient(ABC):
    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.headers = headers

    def send_request(self, method: str, endpoint: str = "", json: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method=method, url=url, headers=self.headers, json=json)

        if response.status_code >= 400:
            raise Exception(f"Ошибка при запросе ({method}) к {url}: {response.status_code} — {response.text}")
        
        return response

    @abstractmethod
    def _parse_response(self, response: requests.Response):
        pass
