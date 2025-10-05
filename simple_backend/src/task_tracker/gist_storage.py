import os
import json
from dotenv import load_dotenv
from task_tracker.base_http_client import BaseHTTPClient

load_dotenv()

class GistStorage(BaseHTTPClient):
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        gist_id = os.getenv("GIST_ID")
        url = f"https://api.github.com/gists/{gist_id}"
        super().__init__(token, url)

    def load_data(self):
        gist_data = self.get()
        content = gist_data["files"]["tasks.json"]["content"]
        return json.loads(content)

    def save_data(self, tasks):
        updated_content = json.dumps(tasks, ensure_ascii=False, indent=2)
        payload = {"files": {"tasks.json": {"content": updated_content}}}
        return self.patch(payload)

