import asyncio
from typing import Optional

from v1.services import AbstractYandexMusicService
from .response import Response, create_error_response
from .response_codes import ResponseCodes


# TODO: add handling exceptions
class ArtistConcertsController:
    __yandex_music_service: AbstractYandexMusicService

    def __init__(self, yandex_music_service: AbstractYandexMusicService):
        self.__yandex_music_service = yandex_music_service

    async def get_artists_concerts(self, artists_ids: Optional[list[str]]) -> Response:
        # TODO: handle repetition in artists_ids
        m = {}

        if artists_ids is not None:
            tasks = []

            for i in artists_ids:
                tasks.append(asyncio.create_task(self.__yandex_music_service.parse_artist_concerts(i)))

            result = await asyncio.gather(*tasks)

            for j, i in enumerate(artists_ids):
                m[i] = result[j]

            return Response(result=m)

        return create_error_response("No artists-Ids provided", ResponseCodes.INVALID_INPUT_DATA)
