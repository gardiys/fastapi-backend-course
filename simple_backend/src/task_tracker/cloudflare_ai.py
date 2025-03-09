import os
from dotenv import load_dotenv
from base_http_client import BaseHTTPClient

load_dotenv()


class CloudflareAI(BaseHTTPClient):
    """Клиент для работы с Cloudflare AI."""

    API_URL = "https://api.cloudflare.com/client/v4/accounts/f5f4fb2fbdb07976b38adace2e41cc98/ai/run/@cf/meta/llama-3-8b-instruct"

    def __init__(self):
        self.api_key = os.getenv("CLOUDFLARE_AI_KEY")
        if not self.api_key:
            raise ValueError("API-ключ Cloudflare AI не найден! Проверь .env файл.")

    def get_headers(self) -> dict:
        """Возвращает заголовки запроса."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def get_solution(self, task_text: str) -> str:
        """Запрашивает решение у Cloudflare AI."""
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "Ты помощник, который отвечает только на русском языке.",
                },
                {
                    "role": "user",
                    "content": f"Как можно решить эту задачу? {task_text}",
                },
            ],
            "temperature": 0.7,
        }
        response = self.request("POST", self.API_URL, payload)
        return (
            response.get("result", {})
            .get("response", "Ошибка генерации ответа")
            .strip()
        )
