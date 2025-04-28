from typing import List, Optional
from task_tracker.models import Task
import httpx



class RemoteTaskStorage:
    def __init__(self, bin_id: str, api_key: str):
        self.base_url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        self.headers = {
            "X-Master-Key": api_key,
            "Content-Type": "application/json"
        }

    
    
    async def save_all(self, tasks: List[Task]):
        payload = [task.model_dump() for task in tasks]
        async with httpx.AsyncClient() as client:
            response = await client.put(self.base_url, headers=self.headers, json={"record": payload})
            response.raise_for_status()



    async def get_all(self) -> List[Task]:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            import json
            raw_data = response.json()["record"]
            if isinstance(raw_data, str):
                data = json.loads(raw_data)
            else:
                data = raw_data
            return [Task(**item) for item in data]

    
    async def add(self, task: Task):
        tasks = await self.get_all()
        if any(t.id == task.id for t in tasks):
            raise ValueError('задача с таким индификатором уже существует')
        tasks.append(task)
        await self.save_all(tasks)

    async def update(self, task_id: int, updated: Task) -> Optional[Task]:
        tasks = await self.get_all()
        for i, t in enumerate(tasks):
            if t.id == task_id:
                tasks[i] = updated
                await self.save_all(tasks)
                return updated
        return None

    async def delete(self, task_id: int) -> Optional[Task]:
        tasks = await self.get_all()
        for t in tasks:
            if t.id == task_id:
                tasks.remove(t)
                await self.save_all(tasks)
                return t
        return None
                        
              
