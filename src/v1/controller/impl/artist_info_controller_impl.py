from typing import Optional

from fastapi import Query

from ..artist_info_controller import ArtistInfoController
from ..response import Response
from ...services import ArtistsService


class ArtistInfoControllerImpl(ArtistInfoController):
    __artists_service: ArtistsService

    def __init__(self, artists_service: ArtistsService):
        self.__artist_service = artists_service

    def get_artist_info_single(self, artist_id: int) -> Response:
        return Response(f'Artist info for {artist_id}')

    def get_artist_info_multiple(self, artist_id: Optional[list[int]] = Query(None)) -> Response:
        return Response(f'Artist info for {artist_id}')
