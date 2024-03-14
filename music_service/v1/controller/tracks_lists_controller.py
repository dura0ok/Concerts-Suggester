from ..service.yandex_music_service import YandexMusicService, NotFoundException, InternalServiceErrorException
from .response import Response, create_error_response
from .response_codes import ResponseCodes


class TracksListController:
    __yandex_music_service: YandexMusicService

    def set_yandex_music_service(self, yandex_music_service: YandexMusicService):
        self.__yandex_music_service = yandex_music_service

    async def get_tracks_list(self, tracks_list_url: str) -> Response:
        return create_error_response('246', ResponseCodes.NOT_FOUND_ERROR)

    async def get_tracks_list_multiple(self, tracks_list_url: list[str]) -> list[dict[str, Response]]:
        return []
