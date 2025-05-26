from base_http_client import BaseHTTPClient

class LLMClient(BaseHTTPClient):
    def __init__(self, api_key: str):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        model = "@cf/meta/llama-3-8b-instruct"
        base_url = f"https://api.cloudflare.com/client/v4/accounts/bf05c539c3c876ed195970a11b785cab/ai/run/{model}"
        super().__init__(base_url, headers)

    def explain(self, task_text: str) -> str:
        payload = {
            "messages": [
                {"role": "system", "content": "Помоги решить и оптимизировать задачу"},
                {"role": "user", "content": task_text}
            ]
        }
        response = self._post("", json=payload)
        return response["result"]["response"]

    def perform_action(self, task_text: str):
        return self.explain(task_text)
