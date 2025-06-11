import requests
from dotenv import load_dotenv
import os
from typing import Optional, Any
from functools import lru_cache
from http_client import BaseHTTPClient

load_dotenv()

class CloudflareAI(BaseHTTPClient):
    def __init__(self):
        super().__init__()
        self.api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        self.model = "@cf/meta/llama-3-8b-instruct"
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def _prepare_request_data(self, task_description: str) -> dict[str, Any]:
        return {
            "messages": [
                {"role": "system", "content": "Ты полезный помощник."},
                {"role": "user", "content": f"Задача: {task_description}. Дай 2-3 совета."}
            ]
        }

    def _process_response(self, response_data: dict[str, Any]) -> Optional[str]:
        result = response_data.get("result", {})
        return result.get("response")

    def get_task_solution_suggestions(self, task_description: str) -> Optional[str]:
        response = self._make_request(
            "POST", f"/{self.model}", self._prepare_request_data(task_description))
        return self._process_response(response) if response else None
