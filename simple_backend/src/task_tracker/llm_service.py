import requests
from typing import Any, Dict, Optional
from base_client import BaseHTTPClient, HTTPError


class LLMService(BaseHTTPClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.cloudflare.com/client/v4/accounts/84345449372656be4199f39b5fd4a832/ai/run/"
        self.model = "@cf/meta/llama-3-8b-instruct"

    def get(self, url: str) -> Dict[str, Any]:
        return self._make_request("GET", url)

    def post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("POST", url, data)

    def put(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("PUT", url, data)

    def get_task_solution(self, task_text: str) -> Optional[str]:
        """Получить рекомендации по решению задачи от LLM."""
        try:
            inputs = [
                {"role": "system", "content": "Ты - помощник по планированию задач. Твоя задача - анализировать задачи и предлагать пошаговые планы их решения."},
                {"role": "user", "content": f"Проанализируй следующую задачу и предложи пошаговый план её решения: {task_text}"}
            ]

            result = self.post(
                f"{self.base_url}{self.model}",
                {"messages": inputs}
            )
            
            response = result.get("result", {}).get("response", "")
            if not response:
                print("Получен пустой ответ от LLM")
                return None
            return response
            
        except HTTPError as e:
            print(f"Ошибка при запросе к LLM: {e.message}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка при работе с LLM: {str(e)}")
            return None
