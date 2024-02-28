from typing import Optional

from fastapi import Query

from ..response import Response
from ..tracklist_artists_controller import TracklistArtistsController
from ...services import ArtistsService, YandexMusicService


class TracklistArtistsControllerImpl(TracklistArtistsController):
    __artists_service: ArtistsService
    __yandex_music_service: YandexMusicService

    def __init__(self, artists_service: ArtistsService, yandex_music_service: YandexMusicService):
        self.__artist_service = artists_service
        self.__yandex_music_service = yandex_music_service

    def get_tracklist_artists_single(self, tracklist_url: str) -> Response:
        return Response(f'Artists of tracklist {tracklist_url}')

    def get_tracklist_artists_multiple(self, tracklist_url: Optional[list[str]] = Query(None)) -> Response:
        return Response(f'Artists of tracklists {tracklist_url}')
