__all__ = ['YandexMusicServiceImpl']


import re
from datetime import datetime
from typing import Optional, Any

import aiohttp

from music_service.v1.service.yandex_music_service.exceptions import NotFoundException, InternalServiceErrorException
from music_service.v1.service.yandex_music_service.yandex_music_service import YandexMusicService
from music_service.v1.model.dto import ConcertDTO, PriceDTO, ArtistDTO, TracksListDTO


def get_dict_value(d: dict, key: str) -> Any:
    """
    Returns value from dictionary by key.

    :param d: dictionary.
    :param key: key of dictionary.
    :raises KeyError: the key is not presented in dictionary.
    """

    return d[key]


def get_dict_value_or_none(d: dict, key: str) -> Any:
    """
    Returns value from dictionary by key or None if the key is not presented in dictionary.

    :param d: dictionary.
    :param key: key of dictionary.
    """

    return d.get(key)


def contains_key(d: dict, key: str) -> bool:
    """
    Returns whether dictionary contains key.

    :param d: dictionary.
    :param key: key of dictionary.
    """

    return d.get(key) is not None


class YandexMusicServiceImpl(YandexMusicService):
    """
    Class represents implementation of :class:`YandexMusicService`.
    """

    __session: aiohttp.ClientSession
    __base_url: str = 'https://api.music.yandex.net'
    __playlist_url_pattern: re.Pattern = re.compile(r"^.*/users/(\S+)/playlists/(\S+)$")
    __album_url_pattern: re.Pattern = re.compile(r"^.*/album/(\S+)$")

    def __init__(self):
        self.__session = aiohttp.ClientSession(base_url=self.__base_url)

    async def parse_tracks_list(self, tracks_list_url: str) -> TracksListDTO:
        playlist_match: re.Match = re.match(self.__playlist_url_pattern, tracks_list_url)
        if playlist_match is not None:
            return await self.__parse_playlist(
                url=tracks_list_url,
                user_id=playlist_match.group(1),
                playlist_id=playlist_match.group(2)
            )

        album_math_match: re.Match = re.match(self.__album_url_pattern, tracks_list_url)
        if album_math_match is not None:
            return await self.__parse_album(
                url=tracks_list_url,
                album_id=album_math_match.group(1)
            )

        raise NotFoundException(f'Tracks list "{tracks_list_url}" not found')

    async def parse_concerts(self, artist_id: int) -> list[ConcertDTO]:
        uri: str = self.__create_artist_brief_info_api_uri(artist_id)
        not_found_message: str = f'Artist "{artist_id}" not found'
        yandex_music_json: dict = await self.__fetch_artist_data(uri=uri, not_found_message=not_found_message)

        try:
            concerts: list[dict] = get_dict_value(yandex_music_json, 'concerts')
            return [self.__extract_concert(c) for c in concerts]
        except Exception as e:
            raise InternalServiceErrorException(f'Parsing concerts of artist "{artist_id}" failed') from e

    async def parse_artist(self, artist_id: int) -> ArtistDTO:
        uri: str = self.__create_artist_api_uri(artist_id)
        not_found_message: str = f'Artist "{artist_id}" not found'
        yandex_music_json: dict = await self.__fetch_artist_data(uri=uri, not_found_message=not_found_message)

        try:
            return self.__extract_artist(get_dict_value(yandex_music_json, 'artist'))
        except Exception as e:
            raise InternalServiceErrorException(f'Parsing info about artist "{artist_id}" failed') from e

    async def terminate(self) -> None:
        await self.__session.close()

    async def __parse_playlist(self, url: str, user_id: str, playlist_id: str) -> TracksListDTO:
        """
        Parses Yandex Music playlist and returns :class:`TracksListDTO`.

        :param url: URL of playlist.
        :param user_id: id of playlist owner on Yandex Music.
        :param playlist_id: id of playlist on Yandex Music.
        :raises NotFoundException: playlist not found (it can by private, for example).
        :raises InternalServiceErrorException: internal error occurred during parsing the playlist.
        """

        uri: str = self.__create_playlist_api_uri(user_id=user_id, playlist_id=playlist_id)
        not_found_message: str = f'Playlist "{url}" not found'

        yandex_music_api_data: dict = await self.__fetch_yandex_music_api_data(
            uri=uri,
            not_found_message=not_found_message
        )

        try:
            return self.__extract_playlist(url=url, playlist=yandex_music_api_data)
        except Exception as e:
            raise InternalServiceErrorException(f'Parsing playlist "{url}" failed') from e

    async def __parse_album(self, url: str, album_id: str) -> TracksListDTO:
        """
        Parses Yandex Music album and returns :class:`TracksListDTO`.

        :param url: URL of album.
        :param album_id: id of album on Yandex Music.
        :raises NotFoundException: album not found.
        :raises InternalServiceErrorException: internal error occurred during parsing the album.
        """

        uri: str = self.__create_album_api_uri(album_id)
        not_found_message: str = f'Album "{url}" not found'

        yandex_music_api_data: dict = await self.__fetch_yandex_music_api_data(
            uri=uri,
            not_found_message=not_found_message
        )

        if get_dict_value_or_none(yandex_music_api_data, 'error'):
            raise NotFoundException(not_found_message)

        try:
            return self.__extract_album(url=url, album=yandex_music_api_data)
        except Exception as e:
            raise InternalServiceErrorException(f'Parsing album "{url}" failed') from e

    async def __fetch_artist_data(self, uri: str, not_found_message: str) -> dict:
        """
        Fetches data from Yandex Music API, checks whether response contains valid data of artist.
        If yes, returns response, else - raises exception.

        In some cases Yandex Music API responds with HTTP-status 200, but really data not found
        (and it can be read from response in some JSON-fields). This method fetches data and checks JSON-content,
        and if there is invalid data, it raises exception as data not found.

        :param uri: URI for Yandex Music API.
        :param not_found_message: message that must be passed to exceptions in case data not found.
        :raises NotFoundException: data not found.
        :raises InternalServiceErrorException: internal error occurred during checking response.
        """

        artist_key: str = 'artist'

        result: dict = await self.__fetch_yandex_music_api_data(
            uri=uri,
            not_found_message=not_found_message
        )

        # It means that Yandex Music API returned unexpected response
        if not contains_key(result, artist_key):
            raise InternalServiceErrorException(f'Response from {uri} does not contains key "{artist_key}"')

        artist_dict: dict = get_dict_value(result, artist_key)

        # It means that Yandex Music API returned artist with error-key, so really this artist not found
        if get_dict_value_or_none(artist_dict, 'error'):
            raise NotFoundException(not_found_message)

        return result

    async def __fetch_yandex_music_api_data(self, uri: str, not_found_message: str) -> dict:
        """
        Fetches dictionary data (in JSON) from Yandex Music API.

        :param uri: URI to be fetched from.
        :param not_found_message: message that must be passed to exception in case data not found.
        :raises NotFoundException: data not found.
        :raises InternalServiceErrorException: internal error during fetching data.
        """

        result_key: str = 'result'

        try:
            response: aiohttp.ClientResponse = await self.__session.get(url=uri)
            response_json: dict = await response.json()
        except Exception as e:
            raise InternalServiceErrorException(f'Downloading {uri} failed') from e
        else:
            status: int = response.status

            is_status_ok: bool = 200 <= status <= 299
            is_status_client_error: bool = 400 <= status <= 499

            if is_status_ok:
                result: Optional[dict] = get_dict_value_or_none(response_json, result_key)
                if result:
                    return result

                raise InternalServiceErrorException(f'Key "{result_key}" not found in response from Yandex Music API')

            if is_status_client_error:
                raise NotFoundException(not_found_message)

            # Got unexpected HTTP-code
            raise InternalServiceErrorException(f'Yandex Music API returned "{status} {response.reason}" for {uri}')

    @staticmethod
    def __extract_concert(concert: dict) -> ConcertDTO:
        """
        Extracts :class:`ConcertDTO` from Yandex Music API JSON-dictionary of concert.

        :param concert: Yandex Music API JSON-dictionary of concert.
        :raises KeyError: Yandex Music API JSON-dictionary doesn't have all required keys.
        """

        concert_datetime_dict: Optional[str] = get_dict_value_or_none(concert, 'datetime')
        if concert_datetime_dict:
            concert_datetime: Optional[datetime] = datetime.strptime(concert_datetime_dict, '%Y-%m-%dT%H:%M:%S%z')
        else:
            concert_datetime: Optional[datetime] = None

        concert_images: Optional[list[str]] = get_dict_value_or_none(concert, 'images')
        concert_artist: dict[str] = get_dict_value(concert, 'artist')

        concert_min_price_dict: Optional[dict] = get_dict_value_or_none(concert, 'minPrice')
        if concert_min_price_dict:
            concert_min_price_value: int = int(get_dict_value(concert_min_price_dict, 'value'))
            concert_min_price_currency = get_dict_value(concert_min_price_dict, 'currency')
            min_price: Optional[PriceDTO] = PriceDTO(price=concert_min_price_value, currency=concert_min_price_currency)
        else:
            min_price: Optional[PriceDTO] = None

        return ConcertDTO(
            title=get_dict_value(concert, 'concertTitle'),
            afisha_url=get_dict_value(concert, 'afishaUrl'),
            city=get_dict_value_or_none(concert, 'city'),
            place=get_dict_value_or_none(concert, 'place'),
            address=get_dict_value_or_none(concert, 'address'),
            datetime=concert_datetime,
            map_url=get_dict_value_or_none(concert, 'mapUrl'),
            images=concert_images if concert_images is not None else [],
            min_price=min_price,
            artists=[YandexMusicServiceImpl.__extract_artist(concert_artist)]
        )

    @staticmethod
    def __extract_playlist(url: str, playlist: dict) -> TracksListDTO:
        """
        Extracts :class:`TracksListDTO` from Yandex Music API JSON-dictionary of playlist.

        :param url: URL of playlist (passed just to be put to :class:`TracksListDTO`).
        :param playlist: Yandex Music API JSON-dictionary of playlist.
        :raises KeyError: Yandex Music API JSON-dictionary doesn't have all required keys.
        """

        artists: set[ArtistDTO] = set()
        for short_track in get_dict_value(playlist, 'tracks'):
            track: dict = get_dict_value(short_track, 'track')
            for a in get_dict_value(track, 'artists'):
                artists.add(YandexMusicServiceImpl.__extract_artist(a))

        return TracksListDTO(
            url=url,
            title=get_dict_value(playlist, 'title'),
            image_link=None,  # TODO
            artists=list(artists)
        )

    @staticmethod
    def __extract_album(url: str, album: dict) -> TracksListDTO:
        """
        Extracts :class:`TracksListDTO` from Yandex Music API JSON-dictionary of album.

        :param url: URL of album (passed just to be put to :class:`TracksListDTO`).
        :param album: Yandex Music API JSON-dictionary of album.
        :raises KeyError: Yandex Music API JSON-dictionary doesn't have all required keys.
        """

        artists: list[dict] = get_dict_value(album, 'artists')

        return TracksListDTO(
            url=url,
            title=get_dict_value(album, 'title'),
            image_link=None,  # TODO
            artists=list(set([YandexMusicServiceImpl.__extract_artist(a) for a in artists]))
        )

    @staticmethod
    def __extract_artist(artist: dict) -> ArtistDTO:
        """
        Extracts :class:`ArtistDTO` from Yandex Music API JSON-dictionary of artist.

        :param artist: Yandex Music API JSON-dictionary of artist.
        :raises KeyError: Yandex Music API JSON-dictionary doesn't have all required keys.
        """

        return ArtistDTO(
            name=get_dict_value(artist, 'name'),
            yandex_music_id=get_dict_value(artist, 'id')
        )

    @staticmethod
    def __create_artist_brief_info_api_uri(artist_id: int) -> str:
        """
        Returns URL of artist's brief info on Yandex Music.

        :param artist_id: id of artist on Yandex Music.
        """

        return f'/artists/{artist_id}/brief-info'

    @staticmethod
    def __create_artist_api_uri(artist_id: int) -> str:
        """
        Returns URL of artist on Yandex Music.

        :param artist_id: id of artist on Yandex Music.
        """

        return f'/artists/{artist_id}'

    @staticmethod
    def __create_playlist_api_uri(user_id: str, playlist_id: str) -> str:
        """
        Returns URL of playlist on Yandex Music.

        :param user_id: id of user on Yandex Music.
        :param playlist_id: id of user's playlist on Yandex Music.
        """

        return f'/users/{user_id}/playlists/{playlist_id}'

    @staticmethod
    def __create_album_api_uri(album_id: str) -> str:
        """
        Returns URL of album on Yandex Music.

        :param album_id: id of album on Yandex Music.
        """

        return f'/albums/{album_id}'
