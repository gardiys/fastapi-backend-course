from BaseHTTPClient import BaseHTTPClient


class LLMclient(BaseHTTPClient):
    def __init__(self, token: str = '',
                 acc_id: str = '7d9cfc61c95bbd1b33a6c5f997a2e213', model_ai: str = 'llama-3.1-8b-instruct'):
        self.acc_id = acc_id
        self.model_ai = model_ai
        self.token = token
        api_url = f'https://api.cloudflare.com/client/v4/accounts/{self.acc_id}/ai/run/@cf/meta/{self.model_ai}'
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        super().__init__(api_url, headers)

    async def get_explain_task(self, task):
        prompt = f"Объясни, что нужно сделать в задаче: '{task['title']}' простыми словами."
        payload = {"messages": [{"role": "user", "content": prompt}]}
        response = await self.post(payload)
        data = response.json()
        task['title'] = data['result']['response']
        return task

    async def custom_method(self):
        pass