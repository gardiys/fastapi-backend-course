from typing import Optional
from base_client import BaseHTTPClient

class CloudflareLLMClient(BaseHTTPClient):
    """Клиент для работы с Cloudflare Workers AI API"""
    
    def __init__(self, api_token: str, account_id: str):
        self.api_token = api_token
        self.account_id = account_id
        base_url = "https://api.cloudflare.com/client/v4"
        super().__init__(base_url)
        
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        # Исправлено: используем self.account_id
        self.model_endpoint = f"/accounts/{self.account_id}/ai/run/@cf/meta/llama-3.1-8b-instruct"

    def load_tasks(self):
        """
        Этот метод не используется для LLM, но должен быть реализован
        из-за абстрактного базового класса
        """
        raise NotImplementedError("LLM клиент не поддерживает загрузку задач")

    def save_tasks(self, data):
        """
        Этот метод не используется для LLM, но должен быть реализован
        из-за абстрактного базового класса
        """
        raise NotImplementedError("LLM клиент не поддерживает сохранение задач")

    def ask_llm(self, prompt: str) -> Optional[str]:
        """
        Отправляет запрос к LLM Cloudflare и возвращает ответ
        """
        kwargs = {
            "headers": self.headers,
            "json": {"prompt": prompt},
            "timeout": 30
        }
        
        response = self._make_request("POST", self.model_endpoint, **kwargs)
        
        if response:
            return response.get("result", {}).get("response")
        return None