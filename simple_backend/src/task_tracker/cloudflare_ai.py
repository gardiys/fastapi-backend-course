import os
import requests
from dotenv import load_dotenv

load_dotenv()


class CloudflareAI:
    """
    Класс для работы с Cloudflare AI.
    Отправляет текст задачи и получает ответ на русском языке.
    """

    API_URL = "https://api.cloudflare.com/client/v4/accounts/f5f4fb2fbdb07976b38adace2e41cc98/ai/run/@cf/meta/llama-3-8b-instruct"

    def __init__(self):
        self.api_key = os.getenv("CLOUDFLARE_AI_KEY")
        if not self.api_key:
            raise ValueError("API-ключ Cloudflare AI не найден! Проверь .env файл.")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def get_solution(self, task_text: str) -> str:
        """
        Отправляет запрос в Cloudflare AI и получает ответ.
        """
        if not task_text.strip():
            return "Ошибка: текст задачи должен быть непустым."

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
            response = requests.post(self.API_URL, json=payload, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            if "result" in data and isinstance(data["result"], dict):
                return data["result"].get("response", "Ошибка генерации ответа").strip()

            return "Ошибка: Cloudflare AI не вернул корректный ответ."

        except requests.RequestException:
            return "Ошибка при запросе к Cloudflare AI."
