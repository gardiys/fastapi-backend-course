import aiohttp

from config import settings


class JSONBinService:
    MASTER_KEY_HEADER_NAME: str = "X-Master-Key"
    ACCESS_KEY_HEADER_NAME: str = "X-Access-Key"
    CONTENT_TYPE_HEADER_NAME: str = "Content-Type"
    CONTENT_TYPE_HEADER_VALUE: str = "application/json"

    def __init__(self, bin_id: str, access_key: str, master_key: str):
        self.bin_id = bin_id
        self.access_key = access_key
        self.master_key = master_key

    @property
    def bin_url(self) -> str:
        return f"{settings.JSONBIN_ROOT_URL}/b/{self.bin_id}"

    async def load_entities(self) -> list[dict[str, int | str]]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.bin_url,
                headers={
                    self.MASTER_KEY_HEADER_NAME: self.master_key,
                    self.ACCESS_KEY_HEADER_NAME: self.access_key,
                },
            ) as response:
                response_body = await response.json()
                return [] if not response_body["record"][0] else response_body["record"]

    async def dump_entities(self, entities: list[dict[str, int | str]]) -> None:
        async with aiohttp.ClientSession() as session:
            await session.put(
                url=self.bin_url,
                json=entities if entities else [{}],
                headers={
                    self.MASTER_KEY_HEADER_NAME: self.master_key,
                    self.ACCESS_KEY_HEADER_NAME: self.access_key,
                },
            )
