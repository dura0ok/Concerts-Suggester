from abc import ABC, abstractmethod
from typing import Optional

from fastapi import Query

from .response import Response


class ConcertsController(ABC):
    @abstractmethod
    def get_artist_concerts_single(self, artist_id: int) -> Response:
        pass

    @abstractmethod
    def get_artist_concerts_multiple(self, artist_id: Optional[list[int]] = Query(None)) -> Response:
        pass
