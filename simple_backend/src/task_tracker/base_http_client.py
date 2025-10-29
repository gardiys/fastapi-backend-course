from abc import ABC, abstractmethod
import requests
import json

class BaseHTTPClient(ABC):
    def __init__(self):
        self.base_url = self.get_base_url()
        self.headers = self.get_headers()
    
    @abstractmethod
    def get_base_url(self) -> str:
       
        pass
    
    @abstractmethod
    def get_headers(self) -> dict:
        
        pass
    
    def make_request(self, method: str, endpoint: str = "", json_data: dict = None, data: str = None, timeout: int = 30):
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=json_data,
                data=data,
                timeout=timeout
            )
            return response
        except Exception as e:
            raise Exception(f"Request error: {str(e)}")