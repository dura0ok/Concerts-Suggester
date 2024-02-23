from dataclasses import dataclass


@dataclass(frozen=True)
class Artist:
    name: str
    yandex_music_id: int
