import asyncio

from ..service.yandex_music_service import YandexMusicService, NotFoundException, InternalServiceErrorException
from .response import Response, create_error_response
from .response_codes import ResponseCodes
from ..model.dto import ConcertDTO


class ConcertsController:
    __yandex_music_service: YandexMusicService

    def set_yandex_music_service(self, yandex_music_service: YandexMusicService):
        self.__yandex_music_service = yandex_music_service

    async def get_concerts(self, artist_id: int) -> Response:
        try:
            result: list[ConcertDTO] = await self.__yandex_music_service.parse_concerts(artist_id)
            return Response(result=result)
        except NotFoundException as e:
            return create_error_response(str(e), ResponseCodes.NOT_FOUND_ERROR)
        except InternalServiceErrorException as e:
            return create_error_response(f'Internal error: {e}', ResponseCodes.INTERNAL_ERROR)

    async def get_multiple_concerts(self, artist_id: list[int]) -> list[dict[int, Response]]:





        async with asyncio.TaskGroup() as task_group:
            tasks = []

            for id in artist_id:
                tasks.append(task_group.create_task())




            task1 = task_group.create_task()
        task2 = task_group.create_task(another_coro(...))



        return []
