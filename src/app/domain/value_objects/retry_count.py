"""
Retry count value object.
"""

from app.domain.value_objects.base import ValueObject


class RetryCount(ValueObject[int]):
    """Retry count value object."""
