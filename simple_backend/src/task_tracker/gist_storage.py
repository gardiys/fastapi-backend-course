import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

class GistStorage:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.gist_id = os.getenv("GIST_ID")
        self.api_url = f"https://api.github.com/gists/{self.gist_id}"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def load_data(self):
        """Загрузить список задач из Gist"""
        response = requests.get(self.api_url, headers=self.headers)
        response.raise_for_status()
        gist_data = response.json()
        file_content = gist_data["files"]["tasks.json"]["content"]
        return json.loads(file_content)

    def save_data(self, tasks):
        """Сохранить обновлённый список задач в Gist"""
        updated_content = json.dumps(tasks, ensure_ascii=False, indent=2)
        payload = {"files": {"tasks.json": {"content": updated_content}}}
        response = requests.patch(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

