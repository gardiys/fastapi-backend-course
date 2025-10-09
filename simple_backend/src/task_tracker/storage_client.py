# не используется, т.к. локальное хранилище не используется, а используется
# gist_storage.py 

from abc import ABC, abstractmethod
from typing import Any

class StorageClient(ABC):
    @abstractmethod
    def load_data(self) -> Any:
	pass

    @abstractmethod
    def save_data(self, data: Any):
	pass
