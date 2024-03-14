from typing import Optional
from fastapi import Query

from music_service.application import Application
from .service.yandex_music_service import YandexMusicService, YandexMusicServiceImpl
from .controller import ConcertsController, TracksListController, Response


class ApplicationV1(Application):
    __yandex_music_service: YandexMusicService
    __concerts_controller: ConcertsController
    __tracks_list_controller: TracksListController

    def __init__(self):
        super().__init__()

        self.__concerts_controller = ConcertsController()
        self.__tracks_list_controller = TracksListController()

        self.add_api_route(
            path='/concerts',
            endpoint=self.__get_concerts,
            methods=['GET'],
        )

        self.add_api_route(
            path='/concerts/multiple',
            endpoint=self.__get_concerts_multiple,
            methods=['GET'],
        )

        self.add_api_route(
            path='/tracks-list',
            endpoint=self.__concerts_controller.get_concerts,
            methods=['GET'],
        )

        self.add_api_route(
            path='/tracks-list/multiple',
            endpoint=self.__tracks_list_controller.get_tracks_list_multiple,
            methods=['GET'],
        )

    async def on_startup(self) -> None:
        self.__yandex_music_service: YandexMusicService = YandexMusicServiceImpl()
        self.__concerts_controller.set_yandex_music_service(self.__yandex_music_service)
        self.__tracks_list_controller.set_yandex_music_service(self.__yandex_music_service)

    async def on_shutdown(self) -> None:
        await self.__yandex_music_service.terminate()

    async def __get_concerts(self, artist_id: int) -> Response:
        return await self.__concerts_controller.get_concerts(artist_id)

    async def __get_concerts_multiple(self, artist_id: Optional[list[int]] = Query(None)) -> list[dict[int, Response]]:
        if artist_id is None:
            return []

        return await self.__concerts_controller.get_multiple_concerts(artist_id)
