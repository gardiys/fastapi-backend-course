import requests
from typing import Optional
import os

class CloudflareLLMClient:
    def __init__(self, api_token: str = None, account_id: str = None):
        self.api_token = api_token or os.getenv("xQ2khCp_9Qu64OnHAv4LUh2nKnk1WpSKCgYqSdnQ")
        self.account_id = account_id or os.getenv("813f8bf4062b54be426656c53d20d298")
        
        if not self.api_token or not self.account_id:
            raise ValueError("Необходимо указать API токен и Account ID для Cloudflare")
        
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/@cf/meta/llama-3.1-8b-instruct"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def ask_llm(self, prompt: str) -> Optional[str]:
        """
        Отправляет запрос к LLM Cloudflare и возвращает ответ
        """
        try:
            payload = {
                "prompt": prompt
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30 
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result.get("result", {}).get("response")
            
        except requests.RequestException as e:
            print(f"Ошибка при запросе к Cloudflare LLM: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None