from typing import Optional

from ..artists_service import ArtistsService
from ...model.dto import ArtistDTO


class ArtistsServiceImpl(ArtistsService):
    def find_artist_by_id(self, artist_id: int) -> Optional[ArtistDTO]:
        pass

    def find_artist_by_yandex_music_id(self, yandex_music_id: int) -> Optional[ArtistDTO]:
        pass

    def add_artist(self, artist: ArtistDTO) -> int:
        pass

    def delete_artist(self, artist_id: int) -> None:
        pass
