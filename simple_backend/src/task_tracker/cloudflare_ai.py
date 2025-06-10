import requests
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

class CloudflareAI:
    def __init__(self):
        self.api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run"
        self.model = "@cf/meta/llama-2-7b-chat-int8"

    def get_task_solution_suggestions(self, task_description: str) -> Optional[str]:
        """Получаем советы"""
        prompt = f"""
        Ты помощник. Пользователь создает задачу:
        "{task_description}". Кратко предложи 2-3 практических способа решения этой задачи.
        Ответ дай в формате маркированного списка.
        """

        try:
            response = requests.post(
                f"{self.base_url}/{self.model}",
                headers={
                    "Aurhorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json"
                },
                json={"messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"rolee": "user", "content": prompt}
                ]}
            )
            response.raise_for_status()
            return response.json().get("result", {}).get("response")
        except Exception as e:
            print(f"Error calling Cloudflare AI: {e}")
            return None