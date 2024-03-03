from abc import ABC, abstractmethod

from fastapi import FastAPI


class Application(FastAPI, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    async def on_startup(self) -> None:
        pass

    @abstractmethod
    async def on_shutdown(self) -> None:
        pass
