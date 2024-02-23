from dataclasses import dataclass


@dataclass(frozen=True)
class Concert:
    title: str
    afisha_url: str
    city: str
    place: str
    address: str
    datetime: str
    map_url: str
    images: list[str]
    min_price_value: int
    min_price_currency: str
