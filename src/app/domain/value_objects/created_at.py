"""
Created at timestamp value object.
"""

from datetime import datetime
from app.domain.value_objects.base import ValueObject


class CreatedAt(ValueObject[datetime]):
    """Created at timestamp value object."""
