"""
Location information value object.
"""

from dataclasses import dataclass
from typing import Optional

from app.domain.value_objects.base import ValueObject
from app.domain.value_objects.coordinates import Coordinates


@dataclass(frozen=True, slots=True)
class LocationInfo(ValueObject[dict[str, str | Coordinates]]):
    """
    Location information value object.
    """
    region: Optional[str]
    subregion: Optional[str]
    capital: Optional[str]
    coordinates: Optional[Coordinates]
    
    @property
    def value(self) -> dict[str, str | Coordinates]:
        """Return location info as dictionary."""
        return {
            "region": self.region,
            "subregion": self.subregion,
            "capital": self.capital,
            "coordinates": self.coordinates
        }
