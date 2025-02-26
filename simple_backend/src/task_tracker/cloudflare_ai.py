import httpx
from pydantic import BaseModel
from typing import Optional

class CloudflareAI:
    def __init__(self, account_id: str, api_token: str):
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    async def generate_solution(self, task_text: str) -> Optional[str]:
        payload = {
            "model": "@cf/meta/llama-3-8b-instruct",  # Пример модели, уточните в документации
            "prompt": f"Given the following task: '{task_text}', provide a step-by-step solution to complete it.",
            "max_tokens": 500
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                return result.get("result", {}).get("response", "No solution generated")
            except httpx.HTTPStatusError as e:
                print(f"Cloudflare API error: {e.response.text}")
                return None
            except httpx.RequestError as e:
                print(f"Network error with Cloudflare: {str(e)}")
                return None