import os
from base_http_client import BaseHTTPClient

class CloudflareTaskManager(BaseHTTPClient):
    def __init__(self):
        super().__init__()
        self.llm_api_url = "https://api.cloudflare.com/client/v4/accounts/{}/ai/run/".format(
            os.getenv('CLOUDFLARE_ACCOUNT_ID')
        )
        self.llm_api_token = os.getenv('CLOUDFLARE_AI_TOKEN')
        self.llm_model = "@cf/meta/llama-3-8b-instruct"

        if not self.llm_api_token:
            raise ValueError("CLOUDFLARE_AI_TOKEN не установен")

    # Реализация абстрактных методов (заглушки)
    async def get_all(self):
        raise NotImplementedError("This method is not supported for CloudflareTaskManager")

    async def create(self, data):
        return self.create_task(data.get('title', ''))

    async def update(self, id, data):
        raise NotImplementedError("This method is not supported for CloudflareTaskManager")

    async def delete(self, id):
        raise NotImplementedError("This method is not supported for CloudflareTaskManager")

    def _call_llm(self, task_description):
        full_url = f"{self.llm_api_url}{self.llm_model}"
        response = self._sync_request(
            "POST",
            full_url,
            headers={
                "Authorization": f"Bearer {self.llm_api_token}",
                "Content-Type": "application/json"
            },
            json={
                "messages": [
                    {"role": "system", "content": "Ты помощник отвечающий на русском языке, какие советы можешь дать по решению этой задачи?"},
                    {"role": "user", "content": task_description}
                ]
            },
            timeout=100
        )
        return response.json().get('result', {}).get('response', 'No AI response') if response else None

    def create_task(self, task_text):
        ai_solution = self._call_llm(task_text)
        return {
            "original_text": task_text,
            "ai_solution": ai_solution if ai_solution else "AI не ответил",
            "status": "created"
        }