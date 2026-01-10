import os
import requests
from dotenv import load_dotenv
from BaseHTTPClient import BaseHTTPClient
load_dotenv()
class Cloudflare(BaseHTTPClient):
    def __init__(self, api_key: str = None, acc_id: str = None):
        self.api_key = api_key or os.getenv("CLOUDFLARE_API_KEY")
        self.acc_id = acc_id or os.getenv("CLOUDFLARE_ACCOUNT_ID")
        base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.acc_id}/ai/run/@cf/meta/llama-3-8b-instruct"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        super().__init__(base_url=base_url, headers=headers)
    def _make_request(self, text: str):
        payload = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that explains tasks clearly."},
                {"role": "user", "content": text}
            ]
        }
        return self._post(json_data=payload)
    def get_llm_response(self, text:str) -> str:
        try:
            data = self._make_request(text)
            return data.get('result', {}).get('response', "No response")
        except Exception as e:
            print("Error getting LLM response:", e)
            return "Error: wrong API answer"