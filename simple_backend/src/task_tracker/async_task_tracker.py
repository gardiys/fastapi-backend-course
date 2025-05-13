import json
import httpx


class GistStorage:
    def __init__(self, gist_id: str = 'a2f9fc0ede0297205930810916e12432',
                 token: str = 'Напишите свой',
                 filename: str = 'tasks.json'):
        self.gist_id = gist_id
        self.token = token
        self.filename = filename
        self.api_url = f"https://api.github.com/gists/{self.gist_id}"
        self.headers = {"Authorization": f"token {self.token}"}

    async def fetch(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.api_url, headers = self.headers)
            response.raise_for_status()
            gist_data = response.json()
            content = gist_data["files"][self.filename]["content"]
            return json.loads(content)

    async def push(self, data):
        async with httpx.AsyncClient() as client:
            gist_data = {"files": {self.filename: {"content": json.dumps(data, ensure_ascii = False, indent = 4)}}}
            response = await client.patch(self.api_url, json = gist_data, headers = self.headers)
            response.raise_for_status()
            return gist_data

    async def create_new_task(self, title: str):
        tasks = await self.fetch()
        new_id = max((task['id'] for task in tasks), default = -1)+1
        new_task = {"id": new_id, "title": title, "status": 0}
        tasks.append(new_task)
        await self.push(tasks)
        return new_task

    async def update_task(self, task_id: int, title: str, status: int):
        tasks = await self.fetch()
        for task in tasks:
            if task['id'] == task_id:
                task['title'] = title
                task['status'] = status
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