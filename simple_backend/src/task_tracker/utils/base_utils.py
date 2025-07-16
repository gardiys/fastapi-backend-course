from abc import ABC, abstractmethod
from typing import Any

import aiohttp


class BaseHTTPClient(ABC):
    @property
    @abstractmethod
    def base_url(self) -> str:
        pass

    @property
    @abstractmethod
    def headers(self) -> dict[str, str]:
        pass

    async def _get(self, path: str = "") -> dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=f"{self.base_url}{path}",
                headers=self.headers,
            ) as response:
                return await response.json()

    async def _post(self, json: dict[str, Any], path: str = "") -> dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{self.base_url}{path}",
                json=json,
                headers=self.headers,
            ) as response:
                return await response.json()

    async def _put(self, json: dict[str, Any], path: str = "") -> None:
        async with aiohttp.ClientSession() as session:
            await session.put(
                url=f"{self.base_url}{path}",
                json=json,
                headers=self.headers,
            )
