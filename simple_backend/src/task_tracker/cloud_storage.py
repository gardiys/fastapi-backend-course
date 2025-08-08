import requests
from typing import List, Dict, Any

class CloudStorage:
    def __init__(self, bin_id: str, api_key: str):
        self.bin_id = bin_id
        self.api_key = api_key
        self.base_url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        self.headers = {
            "X-Master-Key": api_key,
            "Content-Type": "application/json"
        }

    def load_tasks(self) -> List[Dict[str, Any]]:
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            data = response.json().get("record", [])
            return data if isinstance(data, list) else []
        except requests.RequestException as e:
            print(f"Error loading tasks: {e}")
            return []

    def save_tasks(self, tasks: List[Dict[str, Any]]) -> bool:
        try:
            response = requests.put(
                self.base_url, 
                json=tasks, 
                headers=self.headers
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error saving tasks: {e}")
            return False