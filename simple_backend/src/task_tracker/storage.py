import httpx
from fastapi import HTTPException


class TaskAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    async def get_all(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url)
            return response.json()

    async def create(self, task):
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, json=task)
            return response.json()

    async def update(self, task_id, task):
        async with httpx.AsyncClient() as client:
            response = await client.put(f"{self.base_url}/{task_id}", json=task)
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Task not found")
            return response.json()

    async def delete(self, task_id):
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.base_url}/{task_id}")
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Task not found")
            return {"message": "Task deleted successfully"}
