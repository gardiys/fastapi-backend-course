import os
from base_http_client import BaseHTTPClient
from dotenv import load_dotenv

load_dotenv()


class LLMClient(BaseHTTPClient):
    def __init__(self):
        account_id = os.getenv('CF_ACCOUNT_ID')
        token = os.getenv('CF_API_TOKEN')
        super().__init__(
            base_url=f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-2-7b-chat-int8",
            headers={
                'Authorization': f'Bearer {token}',
                "Content-Type": "application/json"
            }
        )

    def _parse_response(self, response):
        result = response.json()
        return result.get('result', {}).get('response', 'Нет ответа от модели.')

    def get_task_solution(self, task_text: str) -> str:
        prompt = {
            "messages": [
                {"role": "system", "content": "You are an assistant who explains how to solve tasks."},
                {"role": "user", "content": f"Как решать следующую задачу: {task_text}"}
            ]
        }
        response = self.send_request("POST", json=prompt)
        return self._parse_response(response)
