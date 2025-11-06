from cloudflare_ai import BaseHTTPClient
from typing import List


class JSONBinStorage(BaseHTTPClient):
    def __init__(self, bin_id: str, api_key: str):
        self.bin_id = bin_id
        self.api_key = api_key
        base_url = f'https://api.jsonbin.io/v3/b/{self.bin_id}'
        headers = {
            'X-Master-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        super().__init__(base_url, headers)
        self.validate_credentials()

    def validate_credentials(self):
        if not self.bin_id or not self.api_key:
            raise ValueError("JSON_BIN_ID или JSON_API_KEY не найдены")

    def get_service_name(self) -> str:
        return "JSONBin Storage"

    def load_data(self) -> List[dict]:
        result = self._make_request("GET")
        return result.get('record', [])

    def save_data(self, data: List[dict]) -> bool:
        self._make_request("PUT", json=data)
        return True