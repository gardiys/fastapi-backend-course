import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CloudflareLLM:
    def __init__(self):
        self.token = os.getenv("CLOUDFLARE_AUTH_TOKEN")
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        # URL для запуска модели LLM
        self.url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/@hf/meta-llama/meta-llama-3-8b-instruct"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_solution(self, task_text: str) -> str:
        """Отправляем текст задачи в LLM и получаем ответ"""
        payload = {
            "messages": [
                {"role": "system", "content": "You are a friendly assistant"},
                {"role": "user", "content": f"Объясни, как решить эту задачу:\n{task_text}"}
            ]
        }
        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            # Правильное извлечение ответа
            return data.get("result", {}).get("response", "Нет ответа от LLM")
        except requests.exceptions.HTTPError as e:
            print("HTTPError:", e, response.text)
            return f"Ошибка запроса к LLM: {e}"
        except Exception as e:
            print("Other Error:", e)
            return f"Ошибка запроса к LLM: {e}"

