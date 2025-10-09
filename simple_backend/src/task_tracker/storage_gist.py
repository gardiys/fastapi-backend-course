import os
import requests
import json
from dotenv import load_dotenv
from BaseHTTPClient import BaseHTTPClient
load_dotenv()  
GITHUB_API = 'https://api.github.com'
class GistStorage(BaseHTTPClient):
    def __init__(self, token: str = None, gist_id: str = None, filename: str = 'tasks.json'):
        self.token: str = token or os.getenv('GITHUB_TOKEN')
        self.gist_id: str = gist_id or os.getenv('GIST_ID')
        self.filename: str = filename
        base_url = f"{GITHUB_API}/gists/{self.gist_id}"
        if not self.token or not self.gist_id:
            raise RuntimeError('GITHUB_TOKEN and GIST_ID must be given')
        headers: dict = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github+json'
        }
        super().__init__(base_url=base_url, headers=headers)
    def _make_request(self, *args, **kwargs):
        pass
    # loading task list from gist
    def load(self) -> list[dict]:
        gist_data = self._get()
        files = gist_data.get("files", {})
        if self.filename not in files:
            return []
        try:
            content = files[self.filename]["content"]
            data = json.loads(content)
            return data.get("tasks", [])
        except json.JSONDecodeError:
            return []
    # saving task list on gist    
    def save(self, tasks: list[dict]) -> None:
        body: dict = {
            'files': {
                self.filename: {
                    'content': json.dumps({'tasks': tasks})
                }
            }
        }
        self._patch(json_data=body)
    # loading task list from gist
    def load(self) -> list[dict]:
        gist_data = self._get()
        files = gist_data.get("files", {})
        if self.filename not in files:
            return []
        try:
            content = files[self.filename]["content"]
            data = json.loads(content)
            return data.get("tasks", [])
        except json.JSONDecodeError:
            return []
    # saving task list on gist    
    def save(self, tasks: list[dict]) -> None:
        body: dict = {
            'files': {
                self.filename: {
                    'content': json.dumps({'tasks': tasks})
                }
            }
        }
        self._patch(json_data=body)