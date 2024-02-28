from abc import ABC, abstractmethod
from typing import Optional

from ..model.dto import ArtistDTO


class ArtistsService(ABC):
    @abstractmethod
    def find_artist_by_id(self, artist_id: int) -> Optional[ArtistDTO]:
        pass

    @abstractmethod
    def find_artist_by_yandex_music_id(self, yandex_music_id: int) -> Optional[ArtistDTO]:
        pass

    @abstractmethod
    def add_artist(self, artist: ArtistDTO) -> int:
        pass

    @abstractmethod
    def delete_artist(self, artist_id: int) -> None:
        pass
