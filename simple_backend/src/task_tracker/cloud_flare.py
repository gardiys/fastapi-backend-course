from typing import Any
from base_http_client import BaseHTTPClient


class CloudflareAIClient(BaseHTTPClient):
    """Клиент для работы с Cloudflare AI API"""

    def __init__(self, account_id: str, api_key: str):
        base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        super().__init__(base_url, headers)

    def load_data(self) -> Any:
        """Не используется для AI клиента, но требуется абстрактным методом"""
        raise NotImplementedError("Метод load_data не реализован для AI клиента")

    def save_data(self, data: Any) -> bool:
        """Не используется для AI клиента, но требуется абстрактным методом"""
        raise NotImplementedError("Метод save_data не реализован для AI клиента")

    def get_task_solutions(self, task_title: str) -> str:
        """Получить способы решения задачи от LLM"""
        prompt = f"""
        Задача: {task_title}

        Проанализируй эту задачу и предложи 3-5 конкретных способов её решения.
        Ответ должен быть кратким, практичным и на русском языке.
        Формат: маркированный список.
        """

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "Ты помощник по решению задач. Давай практичные советы.",
                },
                {"role": "user", "content": prompt},
            ],
            "model": "@cf/meta/llama-3-8b-instruct",
            "max_tokens": 500,
        }

        try:
            result = self._make_request(
                "POST", "/@cf/meta/llama-3-8b-instruct", json=payload
            )
            return result["result"]["response"]
        except Exception:
            return "Не удалось получить рекомендации"
