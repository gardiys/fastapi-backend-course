import os
from base_http_client import BaseHTTPClient

class CloudflareAI(BaseHTTPClient):
    def __init__(self):
        self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')  
        self.api_token = os.getenv('CLOUDFLARE_API_TOKEN')    
        self.model = '@cf/meta/llama-3-8b-instruct'
        super().__init__()
    
    def get_base_url(self) -> str:
        return f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"
    
    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def get_advice(self, task_text: str) -> str:
        """Получает советы по решению задачи от LLM"""
        if not self.account_id or not self.api_token:
            return "AI не настроен"
        
        try:
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "Ты - полезный ассистент. Отвечай ТОЛЬКО на русском языке. Давай четкие, структурированные ответы с нумерованными шагами."
                    },
                    {
                        "role": "user", 
                        "content": f"Дай подробные шаги для решения этой задачи на русском языке: {task_text}"
                    }
                ]
            }
            
            response = self.make_request("POST", json_data=payload, timeout=30)
            
            print(f"Cloudflare Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                return result.get('result', {}).get('response', 'Ответ получен')
            else:
                return f"Ошибка API: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Ошибка: {str(e)}"