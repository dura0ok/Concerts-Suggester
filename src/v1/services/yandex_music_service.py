from abc import ABC, abstractmethod


class YandexMusicService(ABC):
    @abstractmethod
    def parse_concerts(self, artist_id: str) -> None:
        # TODO: add doc
        pass

    @abstractmethod
    async def parse_artists(self, tracks_list_url: str) -> None:
        # TODO: add doc
        pass
