from typing import Any, Dict, List
from base_client import BaseHTTPClient, HTTPError


class CloudStorage(BaseHTTPClient):
    def __init__(self, api_key: str, bin_id: str):
        headers = {
            "X-Master-Key": api_key,
            "Content-Type": "application/json"
        }
        super().__init__(api_key, headers)
        self.bin_id = bin_id
        self.base_url = "https://api.jsonbin.io/v3/b"
    

    def get(self, url: str) -> Dict[str, Any]:
        return self._make_request("GET", url)

    def post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("POST", url, data)

    def put(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("PUT", url, data)

    def delete(self, url):
        return self._make_request("DELETE", url)
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """Загрузить задачи из хранилища."""
        try:
            result = self.get(f"{self.base_url}/{self.bin_id}")
            return result.get("record", [])
        except HTTPError as e:
            print(f"Ошибка при загрузке задач: {e.message}")
            return []

    def save_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Сохранить задачи в хранилище."""
        try:
            result = self.put(f"{self.base_url}/{self.bin_id}", tasks)
            return result.get("record", [])
        except HTTPError as e:
            print(f"Ошибка при сохранении задач: {e.message}")
            return []