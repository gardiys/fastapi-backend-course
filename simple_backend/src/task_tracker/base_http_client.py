from abc import ABC, abstractmethod
import httpx
import requests
from fastapi import HTTPException

class BaseHTTPClient(ABC):
    def __init__(self, base_url=None):
        self.base_url = base_url

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def create(self, data):
        pass

    @abstractmethod
    async def update(self, id, data):
        pass

    @abstractmethod
    async def delete(self, id):
        pass

    async def _async_request(self, method, url, **kwargs):
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, **kwargs)
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Resource not found")
            return response

    def _sync_request(self, method, url, **kwargs):
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return None