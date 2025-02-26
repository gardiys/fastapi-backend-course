from base_http_client import BaseHTTPClient
from typing import Optional

class CloudflareAI(BaseHTTPClient):
    def __init__(self, account_id: str, api_token: str):
        super().__init__()
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    async def perform_action(self, task_text: str) -> Optional[str]:
        payload = {
            "model": "@cf/meta/llama-3-8b-instruct",
            "prompt": f"Given the following task: '{task_text}', provide a step-by-step solution to complete it.",
            "max_tokens": 500
        }
        
        result = await self._make_request("POST", self.base_url, self.headers, payload)
        if result:
            return result.get("result", {}).get("response", "No solution generated")
        return None

    async def generate_solution(self, task_text: str) -> Optional[str]:
        return await self.perform_action(task_text)