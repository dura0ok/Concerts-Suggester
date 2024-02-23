from typing import List, Optional
import re

import yandex_music

from .abstract_yandex_music_service import AbstractYandexMusicService
from v1.model import Concert, Artist


# TODO: add handling exceptions
class DefaultYandexMusicService(AbstractYandexMusicService):
    async def parse_album_owners(self, album_url: str) -> list[Artist]:
        # TODO
        pass

    __playlist_url_pattern: re.Pattern = re.compile(r".*/users/(\S+)/playlists/(\S+)")
    __client: yandex_music.ClientAsync

    def __init__(self):
        self.__client = yandex_music.ClientAsync()

    async def parse_artist_concerts(self, artist_id: str) -> List[Concert]:
        brief_info: Optional[yandex_music.BriefInfo] = await self.__client.artists_brief_info(artist_id=artist_id)

        if brief_info is None:
            return []

        result: list[Concert] = []
        concerts: list[dict] = brief_info.concerts

        for c in concerts:
            images: Optional[list[str]] = c.get('image')
            min_price_dict: Optional[dict] = c.get('min_price')

            result.append(Concert(
                title=c.get('concert_title'),
                afisha_url=c.get('afisha_url'),
                city=c.get('city'),
                place=c.get('place'),
                address=c.get('address'),
                datetime=c.get('datetime'),
                map_url=c.get('map_url'),
                images=images if images else [],
                min_price_value=int(min_price_dict.get('value')) if min_price_dict else None,
                min_price_currency=min_price_dict.get('currency') if min_price_dict else None
            ))

        return result

    async def parse_playlist_artists(self, playlist_url: str) -> set[Artist]:
        match: Optional[re.Match[str]] = re.search(self.__playlist_url_pattern, playlist_url)

        if match is None:
            return set()
        else:
            user_id: str = match.group(1)
            kind: str = match.group(2)

            result: yandex_music.Playlist = await self.__client.users_playlists(kind=kind, user_id=user_id)

            tracks: list[yandex_music.TrackShort] = result.tracks

            ret: set[Artist] = set()

            for t in tracks:
                artists: list[yandex_music.Artist] = t.track.artists

                for a in artists:
                    ret.add(Artist(
                        name=a.name,
                        yandex_music_id=a.id
                    ))

            return ret
