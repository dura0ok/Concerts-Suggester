from music_service.application import Application
from .service.yandex_music_service import YandexMusicService, YandexMusicServiceImpl
from .controller import Controller


class ApplicationV1(Application):
    __yandex_music_service: YandexMusicService
    __controller: Controller

    def __init__(self):
        super().__init__()

        self.__controller = Controller()

        self.add_api_route(
            path='/concerts',
            endpoint=self.__controller.get_concerts,
            methods=['GET']
        )

    async def on_startup(self) -> None:
        self.__yandex_music_service: YandexMusicService = YandexMusicServiceImpl()
        self.__controller.set_yandex_music_service(self.__yandex_music_service)

    async def on_shutdown(self) -> None:
        await self.__yandex_music_service.terminate()
