import json
from pathlib import Path
import requests
from abc import ABC, abstractmethod
from settings import JSONBIN_API_KEY, JSONBIN_BIN_ID, CF_API_TOKEN, CF_ACCOUNT_ID, CF_MODEL

JSONBIN_BASE = "https://api.jsonbin.io/v3/b"
CF_BASE = "https://api.cloudflare.com/client/v4"

class BaseStorage(ABC):
    @abstractmethod
    def load(self):
        pass
    @abstractmethod
    def save(self):
        pass

class TaskStorage(BaseStorage):
    def __init__(self, path: str = "tasks.json"):
        self.path = Path(path)
        if not self.path.exists():
            self.save([])
    def load(self) -> list[dict]:
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)
    def save(self, data: list[dict]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

class RemoteTaskStorage(BaseStorage):
    def __init__(self):
        self.bin_id = JSONBIN_BIN_ID
        self.headers = {"X-Master-Key": JSONBIN_API_KEY, "Content-Type": "application/json"}
    def load(self) -> list[dict]:
        r = requests.get(f"{JSONBIN_BASE}/{self.bin_id}/latest", headers=self.headers, timeout=10)
        r.raise_for_status()
        return r.json()["record"]
    def save(self, data: list[dict]) -> None:
        r = requests.put(f"{JSONBIN_BASE}/{self.bin_id}", headers=self.headers, json=data, timeout=10)
        r.raise_for_status()

class CloudflareAIClient:
    def __init__(self):
        self.url = f"{CF_BASE}/accounts/{CF_ACCOUNT_ID}/ai/run/{CF_MODEL}"
        self.headers = {"Authorization": f"Bearer {CF_API_TOKEN}"}
    def explain(self, text: str) -> str:
        r = requests.post(self.url, headers=self.headers, json={"prompt": text}, timeout=15)
        r.raise_for_status()
        return r.json()["result"]["response"]

