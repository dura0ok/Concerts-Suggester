from abc import ABC, abstractmethod

from ...model.dto import ConcertDTO, ArtistDTO, TracksListDTO


class YandexMusicService(ABC):
    """
    Class represents abstract service for Yandex Music.
    """

    @abstractmethod
    async def parse_tracks_list(self, tracks_list_url: str) -> TracksListDTO:
        """
        Parses playlist/album of Yandex Music.

        :param tracks_list_url: URL of playlist/album of Yandex Music.
        :raises NotFoundException: playlist/album of Yandex Music not found on the URL.
        :raises InternalServiceErrorException: internal service error occurred.
        """

    async def parse_concerts(self, artist_id: int) -> list[ConcertDTO]:
        """
        Parses actual concerts of artist from Yandex Music.

        :param artist_id: id of artist on Yandex Music.
        :raises NotFoundException: artist with this id on Yandex Music not found.
        :raises InternalServiceErrorException: internal service error occurred.
        """

    async def parse_artist(self, artist_id: int) -> ArtistDTO:
        """
        Parses basic information about artist from Yandex Music.

        :param artist_id: id of artist on Yandex Music.
        :raises NotFoundException: artist with this id on Yandex Music not found.
        :raises InternalServiceErrorException: internal service error occurred.
        """

    async def terminate(self) -> None:
        """
        Terminates service and frees all underlying resources.
        """
