from ..service.yandex_music_service import YandexMusicService, NotFoundException, InternalServiceErrorException


class Controller:
    __yandex_music_service: YandexMusicService

    def set_yandex_music_service(self, yandex_music_service: YandexMusicService):
        self.__yandex_music_service = yandex_music_service

    async def get_concerts(self, artist_id: int):
        try:
            return await self.__yandex_music_service.parse_concerts(artist_id)
        except NotFoundException as e:
            return {'Not found'}
        except InternalServiceErrorException as e:
            return {'Internal error'}
