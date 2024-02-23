from typing import Optional

import uvicorn
import fastapi

from config_parsing import ConfigParser, EnvConfigParser
from v1.services import DefaultYandexMusicService
from v1.controller import PlaylistArtistsController, ArtistConcertsController


app = fastapi.FastAPI()
app_v1 = fastapi.FastAPI()

# TODO: add typing
yandex_music_service = DefaultYandexMusicService()
artist_concerts_controller = ArtistConcertsController(yandex_music_service)
playlist_artists_controller = PlaylistArtistsController(yandex_music_service)
config_parser: ConfigParser = EnvConfigParser()


# TODO: move to to package "routing"

@app_v1.get("/playlist-artists")
async def root(url: Optional[list[str]] = fastapi.Query(None)):
    return await playlist_artists_controller.get_playlist_artists(playlists_urls=url)


@app_v1.get("/artist-concerts")
async def root(id: list[str] = fastapi.Query(None)):
    return await artist_concerts_controller.get_artists_concerts(artists_ids=id)


app.mount("/v1", app_v1)

if __name__ == '__main__':
    uvicorn.run(app=app, host=config_parser.parse_host(), port=config_parser.parse_port())
