from dataclasses import dataclass
from typing import Optional

from .artist_dto import ArtistDTO


@dataclass(frozen=True)
class TracksListDTO:
    url: str
    title: str
    image_link: Optional[str]
    artists: list[ArtistDTO]
