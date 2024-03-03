import asyncio
import unittest

from tests.utils import async_test

from music_service.v1.service.yandex_music_service import YandexMusicService, YandexMusicServiceImpl, NotFoundException


class TestYandexMusicServiceImpl(unittest.TestCase):
    __service: YandexMusicService
    __loop: asyncio.AbstractEventLoop

    __known_artists_ids: list[int] = [5, 41191, 42650, 5926594, 6826935]
    __unknown_artists_ids: list[int] = [0, 36807571, 368075711, 3680757111111]

    __known_playlists_urls: list[str] = [
        'https://music.yandex.ru/users/kondrenkokp/playlists/3',
        'https://music.yandex.ru/users/kondrenkokp/playlists/1276',
        'https://music.yandex.ru/users/yamusic-missed/playlists/108077885',
        'https://music.yandex.ru/users/yamusic-premiere/playlists/105588776',
        'https://music.yandex.ru/users/yamusic-bestsongs/playlists/3680757',
        'https://music.yandex.ru/users/yamusic-similar/playlists/3680757',
    ]
    __unknown_playlists_urls: list[str] = [
        'https://music.yandex.ru/users/kondrenkokp/playlists/0'
        'https://music.yandex.ru/users/kondrenkokp/playlists/1273',
        'https://music.yandex.ru/users/kondrenkokp/playlists/13',
        'https://music.yandex.ru/users/kondrenkokp12/playlists/13',
        'https://music.yandex.ru/users/kondrenkokp/playlists/1278',
        'https://music.yandex.ru/users/kondrenkokp/playlists/1278111111111',
    ]

    __known_albums_urls: list[str] = [
        'https://music.yandex.ru/album/10',
        'https://music.yandex.ru/album/29400784',
        'https://music.yandex.ru/album/26736334',
        'https://music.yandex.ru/album/29595560',
        'https://music.yandex.ru/album/4784825',
    ]
    __unknown_albums_urls: list[str] = [
        'https://music.yandex.ru/album/0',
        'https://music.yandex.ru/album/23125'
        'https://music.yandex.ru/album/294007841',
        'https://music.yandex.ru/album/2940078411111',
    ]

    __invalid_tracks_lists_urls: list[str] = [
        '',
        '123456789',
        'https://music.yandex.ru/albu/23125',
        'https://music.yandex.ru/user/kondrenkokp/playlists/1278',
        'https://music.yandex.ru/users/kondrenkokp/playlist/1278',
        'https://music.yandex.ru/users/playlists/',
        'https://music.yandex.ru/album/',
        'https://music.yandex.ru',
    ]

    def setUp(self):
        self.loop = asyncio.get_event_loop()

        async def run():
            self.__service = YandexMusicServiceImpl()

        self.loop.run_until_complete(run())

    @async_test
    async def test_known_artists_info(self):
        for i in self.__known_artists_ids:
            await self.__test_known_artist_info(i)

    @async_test
    async def test_unknown_artists_info(self):
        for i in self.__unknown_artists_ids:
            await self.__test_unknown_artist_info(i)

    @async_test
    async def test_known_artists_concerts(self):
        for i in self.__known_artists_ids:
            await self.__test_known_artist_concerts(i)

    @async_test
    async def test_unknown_artists_concerts(self):
        for i in self.__unknown_artists_ids:
            await self.__test_unknown_artist_concerts(i)

    @async_test
    async def test_known_playlists(self):
        for i in self.__known_playlists_urls:
            await self.__test_known_playlist(i)

    @async_test
    async def test_unknown_playlists(self):
        for i in self.__unknown_playlists_urls:
            await self.__test_unknown_playlist(i)

    @async_test
    async def test_known_albums(self):
        for i in self.__known_albums_urls:
            await self.__test_known_album(i)

    @async_test
    async def test_unknown_albums(self):
        for i in self.__unknown_albums_urls:
            await self.__test_unknown_album(i)

    @async_test
    async def test_invalid_tracks_lists(self):
        for i in self.__invalid_tracks_lists_urls:
            await self.__test_invalid_tracks_list(i)

    def tearDown(self):
        async def run():
            await self.__service.terminate()

        self.loop.run_until_complete(run())

    async def __test_known_artist_info(self, artist_id: int):
        await self.__service.parse_artist(artist_id)

    async def __test_unknown_artist_info(self, artist_id: int):
        try:
            await self.__service.parse_artist(artist_id)
            self.assertTrue(False)
        except NotFoundException as e:
            self.assertRegex(str(e), f'Artist "{artist_id}" not found')

    async def __test_known_artist_concerts(self, artist_id: int):
        await self.__service.parse_concerts(artist_id)

    async def __test_unknown_artist_concerts(self, artist_id: int):
        try:
            await self.__service.parse_concerts(artist_id)
            self.assertTrue(False)
        except NotFoundException as e:
            self.assertRegex(str(e), f'Artist "{artist_id}" not found')

    async def __test_known_album(self, album_url: str):
        await self.__service.parse_tracks_list(album_url)

    async def __test_unknown_album(self, album_url: str):
        try:
            await self.__service.parse_tracks_list(album_url)
            self.assertTrue(False)
        except NotFoundException as e:
            self.assertRegex(str(e), f'Album "{album_url}" not found')

    async def __test_known_playlist(self, playlist_url: str):
        await self.__service.parse_tracks_list(playlist_url)

    async def __test_unknown_playlist(self, playlist_url: str):
        try:
            await self.__service.parse_tracks_list(playlist_url)
            self.assertTrue(False)
        except NotFoundException as e:
            self.assertRegex(str(e), f'Playlist "{playlist_url}" not found')

    async def __test_invalid_tracks_list(self, tracks_list_url: str):
        try:
            await self.__service.parse_tracks_list(tracks_list_url)
            self.assertTrue(False)
        except NotFoundException as e:
            self.assertRegex(str(e), f'Tracks list "{tracks_list_url}" not found')
