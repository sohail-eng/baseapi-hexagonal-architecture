import logging
from dataclasses import dataclass
from datetime import datetime

from app.application.subscription.ports import SubscriptionRepository
from app.application.common.ports.transaction_manager import TransactionManager


log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class InitSubscriptionsRequest:
    pass


class InitSubscriptionsHandler:
    def __init__(
        self,
        subscription_repo: SubscriptionRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._repo = subscription_repo
        self._tx = transaction_manager

    async def execute(self, _request: InitSubscriptionsRequest | None = None) -> list[dict]:
        definitions = [
            {
                "name": "PRO",
                "price": 9.99,
                "subscription_type": "month",
                "currency": "USD",
                "duration": 30,
                "features": {"users": 1, "storage_gb": 10},
                "is_active": True,
                "stripe_price_id": None,
                "stripe_product_id": None,
            },
            {
                "name": "CORPORATE",
                "price": 49.99,
                "subscription_type": "month",
                "currency": "USD",
                "duration": 30,
                "features": {"users": 10, "storage_gb": 100},
                "is_active": True,
                "stripe_price_id": None,
                "stripe_product_id": None,
            },
        ]

        created: list[dict] = []
        now = datetime.utcnow()
        for d in definitions:
            existing = await self._repo.read_by_name(d["name"])
            if existing:
                continue
            new_id = await self._repo.add(
                name=d["name"],
                price=d["price"],
                subscription_type=d["subscription_type"],
                currency=d["currency"],
                duration=d["duration"],
                features=d["features"],
                is_active=d["is_active"],
                stripe_price_id=d["stripe_price_id"],
                stripe_product_id=d["stripe_product_id"],
                created_at=now,
                updated_at=now,
            )
            created.append({"id": new_id, **d})

        await self._tx.commit()
        return created


