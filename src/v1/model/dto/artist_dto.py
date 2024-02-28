from dataclasses import dataclass


@dataclass(frozen=True)
class ArtistDTO:
    name: str
    yandex_music_id: int
