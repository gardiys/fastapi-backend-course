from abc import ABC, abstractmethod
import httpx
from typing import Optional, Any

class BaseHTTPClient(ABC):
    def __init__(self):
        self.client: Optional[httpx.AsyncClient] = None

    async def _make_request(self, method: str, url: str, headers: dict = None, data: dict = None) -> Any:
        if self.client is None:
            self.client = httpx.AsyncClient()
        
        try:
            response = await self.client.request(
                method=method,
                url=url,
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"Network error: {str(e)} - URL: {url}")
            return None

    async def __aenter__(self):
        self.client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
            self.client = None

    @abstractmethod
    async def perform_action(self, *args, **kwargs) -> Any:
        pass