from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .artist_dto import ArtistDTO
from .price_dto import PriceDTO


@dataclass(frozen=True)
class ConcertDTO:
    title: str
    afisha_url: str
    city: Optional[str]
    place: Optional[str]
    address: Optional[str]
    datetime: Optional[datetime]
    map_url: Optional[str]
    images: list[str]
    min_price: Optional[PriceDTO]
    artists: list[ArtistDTO]
