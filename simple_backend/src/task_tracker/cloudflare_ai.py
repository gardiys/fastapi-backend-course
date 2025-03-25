import os
from dotenv import load_dotenv
from base_http_client import BaseHTTPClient

load_dotenv()


class CloudFlareConfig:
    """Конфигурация для работы с Cloudflare API."""
    
    def __init__(self):
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.model = os.getenv("CLOUDFLARE_MODEL")

        if not all([self.api_token, self.account_id, self.model]):
            raise ValueError("❌ Ошибка: Отсутствуют переменные окружения в .env!")


class CloudflareAI(BaseHTTPClient):
    """Клиент для работы с Cloudflare AI."""

    def __init__(self, config: CloudFlareConfig):
        super().__init__()
        self.config = config
        self.api_url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{self.config.account_id}/ai/run/@cf/meta/{self.config.model}"
        )

    def get_headers(self) -> dict:
        """Возвращает заголовки запроса."""
        return {
            "Authorization": f"Bearer {self.config.api_token}",
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



cloudflare_config = CloudFlareConfig()
ai_client = CloudflareAI(cloudflare_config)
