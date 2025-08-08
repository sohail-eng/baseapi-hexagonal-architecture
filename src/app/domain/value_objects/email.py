"""
Email value object.
"""

from app.domain.value_objects.base import ValueObject


class Email(ValueObject[str]):
    """Email value object."""
