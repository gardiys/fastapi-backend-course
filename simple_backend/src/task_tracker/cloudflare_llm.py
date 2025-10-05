import os
from dotenv import load_dotenv
from task_tracker.base_http_client import BaseHTTPClient

load_dotenv()

class CloudflareLLM(BaseHTTPClient):
    def __init__(self):
        token = os.getenv("CLOUDFLARE_AUTH_TOKEN")
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@hf/meta-llama/meta-llama-3-8b-instruct"
        super().__init__(token, url)

    def load_data(self):
        """Для LLM загрузка данных не требуется, поэтому просто возвращаем None"""
        return None

    def save_data(self, data):
        """Для LLM сохранение данных не требуется"""
        return None

    def get_solution(self, task_text: str) -> str:
        payload = {
            "messages": [
                {"role": "system", "content": "You are a friendly assistant"},
                {"role": "user", "content": f"Объясни, как решить эту задачу:\n{task_text}"}
            ]
        }
        try:
            data = self.post(payload)
            return data.get("result", {}).get("response", "Нет ответа от LLM")
        except Exception as e:
            return f"Ошибка запроса к LLM: {e}"

