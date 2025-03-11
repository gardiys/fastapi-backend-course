import requests
from abc import ABC, abstractmethod


class BaseHTTPClient(ABC):
    """Базовый HTTP-клиент для отправки запросов к API."""

    @abstractmethod
    def get_headers(self) -> dict:
        """Метод для получения заголовков, реализуется в наследниках."""
        pass

    def request(self, method: str, url: str, data=None):
        """Отправляет HTTP-запрос и обрабатывает ошибки."""
        try:
            headers = self.get_headers()
            response = requests.request(method, url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Ошибка при запросе: {e}"}
