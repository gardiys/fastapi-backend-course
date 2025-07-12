
from config import settings
from utils.base_utils import BaseHTTPClient


class JSONBinService(BaseHTTPClient):
    MASTER_KEY_HEADER_NAME: str = "X-Master-Key"
    ACCESS_KEY_HEADER_NAME: str = "X-Access-Key"
    CONTENT_TYPE_HEADER_NAME: str = "Content-Type"
    CONTENT_TYPE_HEADER_VALUE: str = "application/json"

    def __init__(self, bin_id: str, access_key: str, master_key: str):
        self.bin_id = bin_id
        self.access_key = access_key
        self.master_key = master_key

    @property
    def base_url(self) -> str:
        return f"{settings.JSONBIN_ROOT_URL}/b/{self.bin_id}"

    @property
    def headers(self) -> dict[str, str]:
        return {
            self.MASTER_KEY_HEADER_NAME: self.master_key,
            self.ACCESS_KEY_HEADER_NAME: self.access_key,
        }

    async def load_entities(self) -> list[dict[str, int | str]]:
        response_body = await self._get()
        return [] if not response_body["record"][0] else response_body["record"]

    async def dump_entities(self, entities: list[dict[str, int | str]]) -> None:
        await self._put(json=entities if entities else [{}])
