from abc import ABC, abstractmethod

from v1.model import Concert, Artist


class AbstractYandexMusicService(ABC):
    @abstractmethod
    def parse_artist_concerts(self, artist_id: str) -> list[Concert]:
        # TODO: add doc
        pass

    @abstractmethod
    async def parse_album_owners(self, album_url: str) -> list[Artist]:
        # TODO: add doc
        pass

    @abstractmethod
    async def parse_playlist_artists(self, playlist_url: str) -> list[Artist]:
        # TODO: add doc
        pass
