import httpx
from abc import ABC, abstractmethod


class BaseHTTPClient(ABC):
    def __init__(self, api_url: str, headers: dict):
        self.api_url = api_url
        self.headers = headers

    async def get(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.api_url, headers = self.headers)
            response.raise_for_status()
            return response

    async def patch(self, json):
        async with httpx.AsyncClient() as client:
            response = await client.patch(self.api_url, json = json, headers = self.headers)
            response.raise_for_status()
            return response

    async def post(self, json):
        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, json = json, headers = self.headers)
            response.raise_for_status()
            return response

    @abstractmethod
    async def custom_method(self):
        pass