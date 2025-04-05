import os
import requests
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class BaseHTTPClient(ABC):
    def __init__(self, api_token):
        self.api_token = api_token

    @abstractmethod
    def get(self, url, headers=None):
        pass

    @abstractmethod
    def post(self, url, headers=None, json=None):
        pass

class CloudflareAPI(BaseHTTPClient):
    def __init__(self, cloudflare_api_token, account_id):
        super().__init__(cloudflare_api_token)
        self.account_id = account_id
        self.base_url = "https://api.cloudflare.com/client/v4"

    def get(self, url, headers=None):
        response = requests.get(url, headers=headers)
        return self._handle_response(response)

    def post(self, url, headers=None, json=None):
        response = requests.post(url, headers=headers, json=json)
        return self._handle_response(response)

    def create_task(self, task_text):
        explanation = self.get_explanation(task_text)

        task_data = {
            "text": f"{task_text}\n\nОбъяснение: {explanation}"
        }

        response = self.post(
            f"{self.base_url}/accounts/{self.account_id}/tasks",
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            },
            json=task_data
        )

        return response

    def get_explanation(self, task_text):
        # Получаем токен из переменной окружения
        huggingface_api_token = os.getenv('HUGGING_FACE_TOKEN')
        
        llm_client = LLMAPI(huggingface_api_token)
        input_text = f"Объясните, как решать задачу: {task_text}"

        return llm_client.post(
            'https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct',
            headers={'Authorization': f'Bearer {llm_client.api_token}'},
            json={"inputs": input_text}
        )

    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            print("Ошибка:", response.status_code, response.text)
            return None


class LLMAPI(BaseHTTPClient):
    def __init__(self, huggingface_api_token):
        super().__init__(huggingface_api_token)

    def get(self, url, headers=None):
        raise NotImplementedError("GET method is not implemented for LLMAPI.")

    def post(self, url, headers=None, json=None):
        response = requests.post(url, headers=headers, json=json)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        else:
            print("Ошибка при получении объяснения:", response.status_code)
            return "Не удалось получить объяснение."
