import json
import os
from base_http_client import BaseHTTPClient

class GistStorage(BaseHTTPClient):
    def __init__(self, filename='tasks.json'):
        self.json_name = filename
        self.gist_id = os.getenv('GIST_ID')  
        self.github_token = os.getenv('GITHUB_TOKEN')
        super().__init__()
    
    def get_base_url(self) -> str:
        return "https://api.github.com"
    
    def get_headers(self) -> dict:
        return {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def load_tasks(self):
        if not self.gist_id or not self.github_token:
            return []
        
        try:
            response = self.make_request("GET", f"/gists/{self.gist_id}")
            
            if response.status_code == 200:
                gist_data = response.json()
                tasks_content = gist_data['files'][self.json_name]['content']
                return json.loads(tasks_content)
            return []
        except:
            return []
    
    def save_tasks(self, task_list):
        if not self.gist_id or not self.github_token:
            return False
        
        try:
            gist_data = {
                "files": {
                    self.json_name: {
                        "content": json.dumps(task_list, indent=2, ensure_ascii=False)
                    }
                }
            }
            
            response = self.make_request(
                "PATCH", 
                f"/gists/{self.gist_id}",
                data=json.dumps(gist_data)
            )
            return response.status_code == 200
        except:
            return False