import os
from dotenv import load_dotenv
from base_http_client import BaseHTTPClient

load_dotenv()

if not all(
    [
        os.getenv("CLOUDFLARE_API_TOKEN"),
        os.getenv("CLOUDFLARE_ACCOUNT_ID"),
        os.getenv("CLOUDFLARE_MODEL"),
    ]
):
    raise ValueError("❌ Ошибка: Отсутствуют переменные окружения в .env!")


class CloudflareAI(BaseHTTPClient):
    """Клиент для работы с Cloudflare AI."""

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("CLOUDFLARE_API_TOKEN")
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        model_name = os.getenv("CLOUDFLARE_MODEL")

        if not self.api_key or not account_id or not model_name:
            raise ValueError("❌ Ошибка: Отсутствуют переменные окружения в .env!")

        self.api_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/{model_name}"

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

        try:
            response = self.request("POST", self.api_url, payload)
            return (
                response.get("result", {})
                .get("response", "❌ Ошибка генерации ответа")
                .strip()
            )
        except Exception as e:
            print(f"❌ Ошибка запроса к Cloudflare AI: {e}")
            return "❌ Ошибка: Невозможно получить ответ от Cloudflare AI."
