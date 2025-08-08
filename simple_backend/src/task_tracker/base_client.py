from abc import ABC, abstractmethod
import requests
from typing import Any, Dict, Optional

class BaseHTTPClient(ABC):
    """Базовый класс для HTTP клиентов с общими функциями"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[Any, Any]]:
        
        """Общий метод для выполнения HTTP запросов"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка HTTP запроса: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None

    @abstractmethod
    def load_tasks(self):
        """Абстрактный метод для загрузки данных"""
        pass

    @abstractmethod
    def save_tasks(self, data):
        """Абстрактный метод для сохранения данных"""
        pass