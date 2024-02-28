from typing import Optional

from fastapi import Query

from ..concerts_controller import ConcertsController
from ..response import Response
from ...services import ArtistsService, YandexMusicService


class ConcertsControllerImpl(ConcertsController):
    __artists_service: ArtistsService
    __yandex_music_service: YandexMusicService

    def __init__(self, artists_service: ArtistsService, yandex_music_service: YandexMusicService):
        self.__artist_service = artists_service
        self.__yandex_music_service = yandex_music_service

    def get_artist_concerts_single(self, artist_id: int) -> Response:
        return Response(f'Concerts for {artist_id}')

    def get_artist_concerts_multiple(self, artist_id: Optional[list[int]] = Query(None)) -> Response:
        return Response(f'Concerts for {artist_id}')
