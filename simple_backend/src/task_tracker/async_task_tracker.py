import json
from BaseHTTPClient import BaseHTTPClient
from LLM_client import LLMclient


class GistStorage(BaseHTTPClient):
    def __init__(self, gist_id: str = 'a2f9fc0ede0297205930810916e12432',
                 token: str = '',
                 filename: str = 'tasks.json'):
        self.filename = filename
        self.gist_id = gist_id
        self.token = token
        api_url = f"https://api.github.com/gists/{self.gist_id}"
        headers = {"Authorization": f"token {self.token}"}
        super().__init__(api_url, headers)
        self.llm_client = LLMclient()

    async def fetch(self):
        response = await self.get()
        gist_data = response.json()
        content = gist_data["files"][self.filename]["content"]
        return json.loads(content)

    async def push(self, data):
        gist_data = {"files": {self.filename: {"content": json.dumps(data, ensure_ascii = False, indent = 4)}}}
        await self.patch(gist_data)
        return gist_data

    async def create_new_task(self, title: str):
        tasks = await self.fetch()
        new_id = max((task['id'] for task in tasks), default = -1)+1
        new_task = {"id": new_id, "title": title, "status": 0}
        explain_task = await self.llm_client.get_explain_task(new_task)
        tasks.append(explain_task)
        await self.push(tasks)
        return new_task

    async def update_task(self, task_id: int, title: str, status: int):
        tasks = await self.fetch()
        for task in tasks:
            if task['id'] == task_id:
                task['title'] = title
                task['status'] = status
                task = await self.llm_client.get_explain_task(task)
                await self.push(tasks)
                return task
        return None

    async def remove_task(self, task_id: int):
        tasks = await self.fetch()
        for task in tasks:
            if task["id"] == task_id:
                deleted = task
                tasks.remove(task)
                await self.push(tasks)
                return deleted
        return None

    async def custom_method(self):
        pass
