from base_http_client import BaseHTTPClient


class CloudTaskStorage(BaseHTTPClient):
    """Класс для хранения задач в jsonbin.io"""

    def __init__(self, bin_id: str, api_key: str):
        base_url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        headers = {"X-Master-Key": api_key, "Content-Type": "application/json"}
        super().__init__(base_url, headers)

    def load_data(self) -> list:
        """Загрузка задач из облака"""
        response_data = self._make_request("GET")
        data = response_data["record"]
        return data.get("tasks", data) if isinstance(data, dict) else data

    def save_data(self, tasks: list) -> bool:
        """Сохранение задач в облаке"""
        data = {"tasks": tasks}
        self._make_request("PUT", json=data)
        return True

    # Для обратной совместимости
    def load_tasks(self):
        return self.load_data()

    def save_tasks(self, tasks):
        return self.save_data(tasks)
