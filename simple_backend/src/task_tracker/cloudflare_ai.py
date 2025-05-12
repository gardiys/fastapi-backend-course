import requests
import os
from dotenv import load_dotenv
from base_client import BaseHTTPClient

load_dotenv()

class CloudflareLLM(BaseHTTPClient):
    def __init__(self):
        CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
        MODEL_NAME = "@cf/meta/llama-2-7b-chat-int8"
        url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/{MODEL_NAME}"
        headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-type": "application/json"
        }
        super().__init__(url, headers)
    
    def solve_task(self, task_text: str) -> str:
        prompt = (
            f"Есть задача: \"{task_text}\"\n\n"
            "Объясни, как можно её решить."
        )
        response = requests.post(self.url, headers=self.headers, json={"prompt": prompt})
        response.raise_for_status()
        data = response.json()
        return data.get("result","")

    def _required_method(self):
        pass
