from abc import ABC, abstractmethod
from typing import Optional

from fastapi import Query

from .response import Response


class TracklistArtistsController(ABC):
    @abstractmethod
    def get_tracklist_artists_single(self, tracklist_url: str) -> Response:
        pass

    @abstractmethod
    def get_tracklist_artists_multiple(self, tracklist_url: Optional[list[str]] = Query(None)) -> Response:
        pass
