import asyncio
from typing import Optional

from v1.services import AbstractYandexMusicService
from .response import Response, create_error_response
from .response_codes import ResponseCodes


# TODO: add handling exceptions
class PlaylistArtistsController:
    __yandex_music_service: AbstractYandexMusicService

    def __init__(self, yandex_music_service: AbstractYandexMusicService):
        self.__yandex_music_service = yandex_music_service

    async def get_playlist_artists(self, playlists_urls: Optional[list[str]]) -> Response:
        # TODO: handle repetition in playlists_urls

        m = {}

        if playlists_urls is not None:
            tasks = []

            for i in playlists_urls:
                tasks.append(asyncio.create_task(self.__yandex_music_service.parse_playlist_artists(i)))

            result = await asyncio.gather(*tasks)

            for j, i in enumerate(playlists_urls):
                m[i] = result[j]

            return Response(result=m)

        return create_error_response(message="No playlist-URLs provided", code=ResponseCodes.INVALID_INPUT_DATA)
