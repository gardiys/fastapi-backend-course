from abc import ABC, abstractmethod
import requests
from typing import Dict, Any, Optional


class BaseHTTPClient(ABC):
    """Базовый класс для HTTP клиентов"""

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = 30

    def _make_request(
        self, method: str, endpoint: str = "", **kwargs
    ) -> Dict[str, Any]:
        """Общий метод для выполнения HTTP запросов"""
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка {method} запроса к {url}: {e}")

    @abstractmethod
    def load_data(self) -> Any:
        """Абстрактный метод для загрузки данных"""
        pass

    @abstractmethod
    def save_data(self, data: Any) -> bool:
        """Абстрактный метод для сохранения данных"""
        pass
