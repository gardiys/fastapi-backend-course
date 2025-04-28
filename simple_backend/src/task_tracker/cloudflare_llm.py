import os
from base_http_client import BaseHTTPClient
import requests


CLOUDFLARE_API_KEY = os.getenv('CLOUDFLARE_API_KEY')
CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/ai/llm"
CLOUDFLARE_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CLOUDFLARE_API_KEY}"
}

if not CLOUDFLARE_API_KEY:
    raise ValueError('API-ключ не найден. Убедитесь, что он указан в .env')

class CloudFlareLLM(BaseHTTPClient):
    def __init__(self):
        super().__init__(CLOUDFLARE_API_URL, CLOUDFLARE_HEADERS)

    def get_solution(self, task_name):
        ask = {"prompt": f"Объясни, как решить следующую задачу: {task_name}"}
        try:
            response = requests.post(self.url, headers=self.headers, json=ask)
            response.raise_for_status()
            return self.process_response(response)
        except requests.RequestException as err:
            return {"error": str(err)}

    def process_response(self, response):
        data = response.json()
        return data.get("solution", "Не удалось получить решение")