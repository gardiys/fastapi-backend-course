import requests

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/bf05c539c3c876ed195970a11b785cab/ai/run/"
headers = {"Authorization": "Bearer BTQqu4KbIo8l8drwgdNmDW1R1ZXvzL9bX3Um6LaK"}
class LLM:

    def __init__(self,task_input):
        self.task_inputs = [{ "role": "system", "content": "Помоги решить и оптимизировать задачу" }
            ,{"role": "user", "content": f'{task_input}'}]
        self.model = "@cf/meta/llama-3-8b-instruct"
    def run(self):
        input = { "messages": self.task_inputs }
        response = requests.post(f"{API_BASE_URL}{self.model}", headers=headers, json=input)
        data = response.json()
        text = data['result']['response']
        print(text)
        return text

