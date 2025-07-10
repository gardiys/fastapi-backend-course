import json
from typing import Any


class JSONFileService:
    def __init__(self, target_file_path: str):
        self.target_file_path = target_file_path

    def load_entities(self) -> list[dict[str, Any]]:
        with open(self.target_file_path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return list()

    def dump_entities(self, entities: list[dict[str, Any]]) -> None:
        with open(self.target_file_path, "w", encoding="utf-8") as file:
            json.dump(entities, file, indent=2)
