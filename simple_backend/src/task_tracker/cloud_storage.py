# cloud_storage.py
from typing import List, Dict, Any
from base_client import BaseHTTPClient

class CloudStorage(BaseHTTPClient):
    
    def __init__(self, bin_id: str, api_key: str):
        self.bin_id = bin_id
        self.api_key = api_key
        base_url = "https://api.jsonbin.io/v3"
        super().__init__(base_url)
        
        self.headers = {
            "X-Master-Key": api_key,
            "Content-Type": "application/json"
        }

    def load_tasks(self) -> List[Dict[str, Any]]:

        endpoint = f"/b/{self.bin_id}"
        kwargs = {"headers": self.headers}
        
        response = self._make_request("GET", endpoint, **kwargs)
        
        if response:
            data = response.get("record", [])
            return data if isinstance(data, list) else []
        return []

    def save_tasks(self, tasks: List[Dict[str, Any]]) -> bool:

        endpoint = f"/b/{self.bin_id}"
        kwargs = {
            "headers": self.headers,
            "json": tasks
        }
        
        response = self._make_request("PUT", endpoint, **kwargs)
        return response is not None