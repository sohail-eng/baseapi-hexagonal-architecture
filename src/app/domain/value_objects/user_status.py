"""
User status value objects.
"""

from app.domain.value_objects.base import ValueObject


class UserActive(ValueObject[bool]):
    """User active status value object."""


class UserBlocked(ValueObject[bool]):
    """User blocked status value object."""


class UserVerified(ValueObject[bool]):
    """User verified status value object."""
