from abc import ABC, abstractmethod


class ConfigParser(ABC):
    @abstractmethod
    def parse_host(self) -> str:
        pass

    @abstractmethod
    def parse_port(self) -> int:
        pass
