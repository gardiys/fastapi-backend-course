import os
import requests
from storage import TaskAPI

class CloudflareTaskManager(TaskAPI):
    def __init__(self):
        self.llm_api_url = "https://api.cloudflare.com/client/v4/accounts/{}/ai/run/".format(
            os.getenv('CLOUDFLARE_ACCOUNT_ID')
        )
        self.llm_api_token = os.getenv('CLOUDFLARE_AI_TOKEN')
        self.llm_model = "@cf/meta/llama-3-8b-instruct"

        if not self.llm_api_token:
            raise ValueError("CLOUDFLARE_AI_TOKEN не установлен")

    def _call_llm(self, task_description):
        try:
            response = requests.post(
                f"{self.llm_api_url}{self.llm_model}",
                headers={
                    "Authorization": f"Bearer {self.llm_api_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "messages": [
                        {"role": "system", "content": "Ты помошник отвечающий на русском языке, какие советы можешь дать по решению этой задачи?"},
                        {"role": "user", "content": task_description}
                    ]
                },
                timeout=100
            )
            response.raise_for_status()
            return response.json().get('result', {}).get('response', 'No AI response')
        except Exception as e:
            print(f"AI request failed: {str(e)}")
            return None

    def create_task(self, task_text):
        ai_solution = self._call_llm(task_text)
        return {
            "original_text": task_text,
            "ai_solution": ai_solution if ai_solution else "AI не ответил",
            "status": "created"
        }