"""
Last login value object.
"""

from datetime import datetime
from app.domain.value_objects.base import ValueObject


class LastLogin(ValueObject[datetime]):
    """Last login value object."""
