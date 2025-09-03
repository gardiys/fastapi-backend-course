import requests


class LLMAssistant:

    def __init__(self, api_key: str, llm_id: str, model: str = "@cf/meta/llama-3-8b-instruct"):
        self.url = f"https://api.cloudflare.com/client/v4/accounts/{llm_id}/ai/run/"
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def assist_llm(self, task_description: str) -> str:
        inputs = {
            "role": "user",
            "prompt": f"Твоя задача:\n{task_description}"
                      f"Напиши с подробным обьяснением как мне выполнить данную задачу. Укладывайся в диапозон в 200 символов"
        }
        response = requests.post(f"{self.url}{self.model}", headers=self.headers, json=inputs)
        return response.json()['result']['response']
