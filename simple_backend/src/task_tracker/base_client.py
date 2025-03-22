from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import requests

class BaseHTTPClient(ABC):
    def __init__(self, api_key: str, headers: Optional[Dict[str, str]] = None):
        self.api_key = api_key
        self.headers = headers or {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    @abstractmethod
    def get(self, url: str) -> Dict[str, Any]:
        """Выполнить GET запрос."""
        pass

    @abstractmethod
    def post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнить POST запрос."""
        pass

    @abstractmethod
    def put(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнить PUT запрос."""
        pass

    def _make_request(self, method: str, url: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Выполнить HTTP запрос с обработкой ошибок."""
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                error_msg = f"Ошибка при запросе {method} {url}: {response.status_code}"
                print(error_msg)
                print("Ответ сервера:", response.text)
                raise HTTPError(error_msg, response.status_code, response.text)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Ошибка сети при запросе {method} {url}: {str(e)}"
            print(error_msg)
            raise HTTPError(error_msg, 0, str(e))
        except Exception as e:
            error_msg = f"Неожиданная ошибка при запросе {method} {url}: {str(e)}"
            print(error_msg)
            raise HTTPError(error_msg, 0, str(e))

class HTTPError(Exception):
    """Исключение для ошибок HTTP запросов."""
    def __init__(self, message: str, status_code: int, response_text: str):
        self.message = message
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(self.message) 