from fastapi import FastAPI

from .controller.impl.artist_info_controller_impl import ArtistInfoControllerImpl
from .controller.impl.concerts_controller_impl import ConcertsControllerImpl
from .controller.impl.tracklist_artists_controller_impl import TracklistArtistsControllerImpl
from .routing import Router
from .services.impl.artists_service_impl import ArtistsServiceImpl
from .services.impl.yandex_music_service_impl import YandexMusicServiceImpl


class ApplicationV1(FastAPI):
    def __init__(self):
        super().__init__()

        artists_service = ArtistsServiceImpl()
        yandex_music_service = YandexMusicServiceImpl()

        tracklist_artists_controller = TracklistArtistsControllerImpl(
            artists_service=artists_service,
            yandex_music_service=yandex_music_service
        )

        concerts_controller = ConcertsControllerImpl(
            artists_service=artists_service,
            yandex_music_service=yandex_music_service
        )

        artist_info_controller = ArtistInfoControllerImpl(
            artists_service=artists_service
        )

        router = Router(
            tracklist_artists_controller=tracklist_artists_controller,
            concerts_controller=concerts_controller,
            artist_info_controller=artist_info_controller
        )
        super().include_router(router)
