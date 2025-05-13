import httpx


class LLMclient:
    def __init__(self, token: str = '',
                 acc_id: str = '7d9cfc61c95bbd1b33a6c5f997a2e213', model_ai: str = 'llama-3.1-8b-instruct'):
        self.acc_id = acc_id
        self.model_ai = model_ai
        self.api_url = f'https://api.cloudflare.com/client/v4/accounts/{self.acc_id}/ai/run/@cf/meta/{self.model_ai}'
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    async def get_expain_task(self, task):
        prompt = f"Объясни, что нужно сделать в задаче: '{task['title']}' простыми словами."
        payload = {
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, headers = self.headers, json = payload)
            response.raise_for_status()
            data = response.json()

            task['title'] = data['result']['response']

            return task
