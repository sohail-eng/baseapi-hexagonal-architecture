from abc import ABC
from dataclasses import dataclass
from typing import Any, TypeVar

from app.domain.exceptions.base import DomainError
from app.domain.value_objects.base import ValueObject

T = TypeVar("T", bound=ValueObject)


@dataclass(eq=False)
class Entity[T: ValueObject](ABC):
    """
    Base class for domain entities, defined by a unique identity (`id`).
    - `id`: Identity that remains constant throughout the entity's lifecycle.
    - Entities are mutable, but are compared solely by their `id`.
    - Subclasses must set `eq=False` to inherit the equality behavior.
    - Add `kw_only=True` in subclasses to enforce named arguments for clarity & safety.
    """

    id_: T

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Prevents modifying the `id` after it's set.
        Other attributes can be changed as usual.
        """
        if name == "id_":
            current = getattr(self, "id_", None)
            # Allow setting if id_ is not set yet, or if placeholder (value==0)
            if current is not None:
                current_value = getattr(current, "value", None)
                if current_value not in (None, 0):
                    raise DomainError("Changing entity ID is not permitted.")
        super().__setattr__(name, value)

    def __eq__(self, other: Any) -> bool:
        """
        Two entities are considered equal if they have the same `id`,
        regardless of other attribute values.
        """
        return type(self) is type(other) and other.id_ == self.id_

    def __hash__(self) -> int:
        """
        Generate a hash based on entity type and the immutable `id`.
        This allows entities to be used in hash-based collections and
        reduces the risk of hash collisions between different entity types.
        """
        return hash((type(self), self.id_))
