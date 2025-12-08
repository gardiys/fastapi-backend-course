import requests
import os

class CloudflareLLMClient:
    def __init__(self, account_id: str, api_key: str):
        self.account_id = account_id
        self.api_key = api_key
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/@cf/meta/llama-3.2-3b-instruct"

    def ask(self, text: str):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "messages": [
                {"role": "system", "content": "Объясни, как выполнять задачу."},
                {"role": "user", "content": text}
            ]
        }

        response = requests.post(self.base_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()["result"]["response"]

