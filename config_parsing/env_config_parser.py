import os
from typing import Optional

from dotenv import load_dotenv

from .config_parser import ConfigParser


class EnvConfigParser(ConfigParser):
    __host_key_name: str = 'HOST'
    __port_key_name: str = 'PORT'

    __default_host: str = '127.0.0.1'
    __default_port: int = 8000

    def __init__(self) -> None:
        load_dotenv()

    def parse_host(self) -> str:
        return os.getenv(EnvConfigParser.__host_key_name) or self.__default_host

    def parse_port(self) -> int:
        port: Optional[str] = os.getenv(EnvConfigParser.__port_key_name)
        return int(port) if port is not None else self.__default_port
