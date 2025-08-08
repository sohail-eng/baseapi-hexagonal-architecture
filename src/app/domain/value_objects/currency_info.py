"""
Currency information value object.
"""

from dataclasses import dataclass
from typing import Optional

from app.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True)
class CurrencyInfo(ValueObject[dict[str, str]]):
    """
    Currency information value object.
    """
    code: str
    name: Optional[str]
    symbol: Optional[str]
    
    @property
    def value(self) -> dict[str, str]:
        """Return currency info as dictionary."""
        return {
            "code": self.code,
            "name": self.name,
            "symbol": self.symbol
        }
