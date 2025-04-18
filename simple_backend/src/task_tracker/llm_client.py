from base_http_client import BaseHTTPClient


class LLMClient(BaseHTTPClient):
    def __init__(self, api_key: str, account_id: str):
        base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3.1-8b-instruct-fast"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        super().__init__(base_url=base_url, headers=headers)

    def parse_response(self, response):
        return response.json().get("result", {}).get("response")

    def ask(self, task_text: str) -> str | None:
        payload = {
            "messages": [
                {"role": "system", "content": "Отвечай кратко в виде списка пунктов"},
                {"role": "user", "content": f"Объясни, как решить задачу: {task_text}"},
            ]
        }
        return self._request(method="POST", json=payload)
