from abc import ABC, abstractmethod


class BaseHTTPClient(ABC):

    @abstractmethod
    def request(self, *args):
        pass
