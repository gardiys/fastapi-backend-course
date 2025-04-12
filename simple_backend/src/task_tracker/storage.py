from base_http_client import BaseHTTPClient

class TaskAPI(BaseHTTPClient):
    async def get_all(self):
        response = await self._async_request("GET", self.base_url)
        return response.json()

    async def create(self, task):
        response = await self._async_request("POST", self.base_url, json=task)
        return response.json()

    async def update(self, task_id, task):
        response = await self._async_request("PUT", f"{self.base_url}/{task_id}", json=task)
        return response.json()

    async def delete(self, task_id):
        response = await self._async_request("DELETE", f"{self.base_url}/{task_id}")
        return {"message": "Task deleted successfully"}