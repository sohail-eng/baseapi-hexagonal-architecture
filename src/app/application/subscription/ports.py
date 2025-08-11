from abc import abstractmethod
from typing import Protocol
from datetime import datetime


class SubscriptionRepository(Protocol):
    @abstractmethod
    async def read_by_name(self, name: str) -> dict | None: ...

    @abstractmethod
    async def add(
        self,
        *,
        name: str,
        price: float,
        subscription_type: str,
        currency: str,
        duration: int,
        features: dict | None,
        is_active: bool,
        stripe_price_id: str | None,
        stripe_product_id: str | None,
        created_at: datetime,
        updated_at: datetime,
    ) -> int: ...

    @abstractmethod
    async def update_stripe_ids(self, *, id_: int, stripe_price_id: str, stripe_product_id: str) -> None: ...


