import os
from typing import Optional

from dotenv import load_dotenv


class ConfigParser:
    __host_key: str = 'HOST'
    __port_key: str = 'PORT'

    def __init__(self) -> None:
        load_dotenv()

    def parse_port(self) -> Optional[int]:
        port_str: Optional[str] = os.getenv(self.__port_key)
        return int(port_str) if port_str else None

    def parse_host(self) -> Optional[str]:
        return os.getenv(self.__host_key)
