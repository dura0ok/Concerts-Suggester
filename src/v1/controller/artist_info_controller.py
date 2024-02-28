from abc import ABC, abstractmethod
from typing import Optional

from fastapi import Query

from .response import Response


class ArtistInfoController(ABC):
    @abstractmethod
    def get_artist_info_single(self, artist_id: int) -> Response:
        pass

    @abstractmethod
    def get_artist_info_multiple(self, artist_id: Optional[list[int]] = Query(None)) -> Response:
        pass
