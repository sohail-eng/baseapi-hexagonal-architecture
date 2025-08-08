"""
Phone number value object.
"""

from app.domain.value_objects.base import ValueObject


class PhoneNumber(ValueObject[str]):
    """Phone number value object."""
