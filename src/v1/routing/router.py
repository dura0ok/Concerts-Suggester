from fastapi import APIRouter

from ..controller import TracklistArtistsController, ConcertsController, ArtistInfoController


class Router(APIRouter):
    def __init__(self,
                 tracklist_artists_controller: TracklistArtistsController,
                 concerts_controller: ConcertsController,
                 artist_info_controller: ArtistInfoController):
        super().__init__()
        self.__add_tracklist_artists_route(tracklist_artists_controller)
        self.__add_artists_route(artist_info_controller)
        self.__add_concerts_route(concerts_controller)

    def __add_tracklist_artists_route(self, controller: TracklistArtistsController) -> None:
        super().add_api_route(
            path='/tracklist-artists',
            endpoint=controller.get_tracklist_artists_single,
            methods=['GET'],
        )

        super().add_api_route(
            path='/tracklist-artists/multiple',
            endpoint=controller.get_tracklist_artists_multiple,
            methods=['GET']
        )

    def __add_artists_route(self, controller: ArtistInfoController) -> None:
        super().add_api_route(
            path='/artist-info',
            endpoint=controller.get_artist_info_single,
            methods=['GET'],
        )

        super().add_api_route(
            path='/artist-info/multiple',
            endpoint=controller.get_artist_info_multiple,
            methods=['GET'],
        )

    def __add_concerts_route(self, controller: ConcertsController) -> None:
        super().add_api_route(
            path='/artist-concerts',
            endpoint=controller.get_artist_concerts_single,
            methods=['GET'],
        )

        super().add_api_route(
            path='/artist-concerts/multiple',
            endpoint=controller.get_artist_concerts_multiple,
            methods=['GET'],
        )
