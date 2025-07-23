import requests

class LLMAssistant:
    def __init__(self, api_token: str):
        self.url = "https://api.cloudflare.com/client/v4/llm/infer"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def task_llm(self, task_text: str):
        body = {
            "prompt": f"Задача: {task_text}. Объясни пошагово, как её выполнить.",
            "max_tokens": 150
        }

        response = requests.post(self.url, json=body, headers=self.headers)
        if response.status_code == 200:
            return response.json()["result"]["response"]
        return "LLM не нашел решение для вашей задачи"