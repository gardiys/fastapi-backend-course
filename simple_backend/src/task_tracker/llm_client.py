import httpx
import asyncio

class CloudflareLLMClient:
    def __init__(self, endpoint_url: str, api_key: str = None):
        self.url = endpoint_url
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    async def get_solution(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(self.url, json={"prompt": prompt}, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "No response from AI")