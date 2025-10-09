from .base_http_client import BaseHTTPClient
from .config import settings

class CloudflareLLM(BaseHTTPClient):
    def __init__(self):
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUDFLARE_ACCOUNT_ID}/ai/run/{settings.CLOUDFLARE_MODEL}"
        super().__init__(token=settings.CLOUDFLARE_AUTH_TOKEN, url=url)

    def get_solution(self, task_text: str) -> str:
        payload = {
            "messages": [
                {"role": "system", "content": "Ты помощник, объясни, как решить задачу"},
                {"role": "user", "content": task_text}
            ]
        }
        response = self.post(payload)
        return response["result"]["response"]
