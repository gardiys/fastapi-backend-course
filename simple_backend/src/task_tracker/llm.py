import requests

from base_client import BaseHTTPClient

class LLMAssistant(BaseHTTPClient):
    def __init__(self, api_token: str):
        url = "https://api.cloudflare.com/client/v4/llm/infer"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        super().__init__(url, headers)

    def task_llm(self, task_text: str):
        body = {
            "prompt": f"Задача: {task_text}. Объясни пошагово, как её выполнить.",
            "max_tokens": 150
        }
        try:
            result = self.post(body)
            return result["result"]["response"]
        except Exception:
            return "LLM не нашел решение для вашей задачи"

    def handle(self, task_text):
        return self.task_llm(task_text)