import requests
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any

class BaseHTTPClient(ABC):
    def __init__(
            self, 
            api_url: str,
            headers: Optional[Dict[str, str]] = None,
            *,
            default_timeout: float = 15.0):
        self.api_url = api_url
        self._headers = headers or {}
        self._default_timeout = float(default_timeout)
        self._session = requests.Session()

    @abstractmethod
    def _default_headers(self) -> Dict[str, str]:
        raise NotImplementedError

    def build_url(self, path: str = "") -> str:
        return self.api_url + path.lstrip("/")
    
    def request(self,
                method: str,
                path: str = "",
                *,
                params: Optional[Dict[str, Any]] = None,
                json: Optional[Any] = None,
                data: Optional[Any] = None,
                headers: Optional[Dict[str, str]] = None,
                timeout: Optional[float] = None) -> requests.Response:
        merged_headers = {**self._headers, **(headers or {})}
        response = self._session.request(method=method.upper(),
                                         url=self.build_url(self.build_url(path)),
                                         params=params,
                                         json=json,
                                         data=data,
                                         headers=merged_headers,
                                         timeout=self._default_timeout if timeout is None else float(timeout))
        return response

    def ensure_ok(self, resp: requests.Response) -> None:
        try:
            resp.raise_for_status()
        except requests.HTTPError as exc:
            raise requests.HTTPError(f"HTTP {resp.status_code}: {resp.text}") from exc

    def get(self, path: str = "", **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)
    
    def post(self, path: str = "", **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str = "", **kwargs) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str = "", **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)