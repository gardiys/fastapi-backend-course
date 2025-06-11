from abc import ABC, abstractmethod
import requests
from typing import Optional, Any


class BaseHTTPClient(ABC):
    def __init__(self):
        self.base_url: str = ""
        self.headers: dict[str, str] = {}
        self.timeout: int = 30

    def _make_request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[dict[str, Any]] = None
    ):
        """Общий метод для выполнения HTTP-запросов"""
        try:
            response = requests.request(
                method,
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                json=json_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"HTTP request error: {e}")
            return None

    @abstractmethod
    def _prepare_request_data(self, *args, **kwargs) -> dict[str, Any]:
        """Абстрактный метод для подготовки данных запроса"""
        pass

    @abstractmethod
    def _process_response(self, response_data: dict[str, Any]) -> Any:
        """Абстрактный метод для обработки ответа"""
        pass
    
    
