from typing import Dict
from base_http_client import BaseHTTPClient


class LLMAssistant(BaseHTTPClient):

    def __init__(self, api_token: str, account_id: str, model: str = "@cf/meta/llama-3-8b-instruct"): 
        self.api_token = api_token
        self.account_id = account_id
        self.model = model
        api_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"
        super().__init__(api_url=api_url, default_timeout=20.0)

    def _default_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_token}"}

    def task_llm(self, task_text: str) -> str:
        input = {"messages": [
            {"role": "system", 
             "content": f"Напиши короткое решение задачи (до 150 символов): {task_text}"}
        ]}

        response = self.post(self.model, json=input)
        
        if response.status_code == 200:
            return response.json().get("result", {}).get("response", "")
        return f"Ошибка LLM: {response.status_code} {response.text}"