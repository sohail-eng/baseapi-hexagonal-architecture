"""
Updated at timestamp value object.
"""

from datetime import datetime
from app.domain.value_objects.base import ValueObject


class UpdatedAt(ValueObject[datetime]):
    """Updated at timestamp value object."""
