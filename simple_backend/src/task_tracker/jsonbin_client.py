from base_http_client import BaseHTTPClient

class JsonDBClient(BaseHTTPClient):
    def __init__(self, api_key: str, bin_id: str):
        headers = {
            "Content-Type": "application/json",
            "X-Master-Key": api_key
        }
        super().__init__(f"https://api.jsonbin.io/v3/b/{bin_id}", headers)

    def get_data(self):
        return self._get()["record"]

    def save_data(self, data: dict):
        return self._put("", json=data)

    def perform_action(self):
        return self.get_data()
