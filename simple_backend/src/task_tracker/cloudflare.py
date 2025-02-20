import requests
import json
import yaml


with open("settings.yml", "r", encoding="utf-8") as file:
    settings = yaml.safe_load(file)


class CloudFlare:
    def __init__(self):
        self.__cloudflare_id = settings.get("cloudflare_id")
        self.__cloudflare_token = settings.get("cloudflare_token")
        self.__cloudflare_url = f"https://api.cloudflare.com/client/v4/accounts/{self.__cloudflare_id}/ai/run/@cf/meta/llama-3-8b-instruct"

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.__cloudflare_token}"}

    def send_prompt(self, task_name):
        try:
            data = {
                "prompt": f"Объясни решение этой задачи на русском языке: {task_name}"
            }

            response = requests.post(
                url=self.__cloudflare_url, headers=self.headers, json=data
            )

            return response.json()["result"]["response"]

        except Exception as e:
            return {"error": str(e)}
