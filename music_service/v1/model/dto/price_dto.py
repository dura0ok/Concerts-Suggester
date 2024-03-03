from dataclasses import dataclass


@dataclass(frozen=True)
class PriceDTO:
    price: int
    currency: str
