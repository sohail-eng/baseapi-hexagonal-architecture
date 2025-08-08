"""
SQLAlchemy mapping for Subscription entity.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, JSON
from sqlalchemy.orm import mapped_column

from app.domain.entities.subscription import Subscription
from app.domain.value_objects.subscription_id import SubscriptionId
from app.domain.value_objects.subscription_name import SubscriptionName
from app.domain.value_objects.price import Price
from app.domain.value_objects.subscription_type import SubscriptionType
from app.domain.value_objects.currency import Currency
from app.domain.value_objects.duration import Duration
from app.domain.value_objects.features import Features
from app.domain.value_objects.subscription_status import SubscriptionStatus
from app.domain.value_objects.stripe_price_id import StripePriceId
from app.domain.value_objects.stripe_product_id import StripeProductId
from app.domain.value_objects.created_at import CreatedAt
from app.domain.value_objects.updated_at import UpdatedAt
from app.infrastructure.persistence_sqla.registry import mapping_registry


def map_subscriptions_table() -> None:
    """Map Subscription entity to database table."""
    
    @mapping_registry.mapped
    class SubscriptionsTable:
        __tablename__ = "subscriptions"
        
        # Primary key
        id = mapped_column(Integer, primary_key=True, index=True)
        
        # Subscription information
        name = mapped_column(String(100), nullable=False)
        price = mapped_column(Float, nullable=False)
        subscription_type = mapped_column(String(100), nullable=False, default="month")
        currency = mapped_column(String(3), default="USD")
        duration = mapped_column(Integer, nullable=False)  # Duration in days
        features = mapped_column(JSON, nullable=True)
        is_active = mapped_column(Boolean, default=True)
        stripe_price_id = mapped_column(String(255), nullable=True)
        stripe_product_id = mapped_column(String(255), nullable=True)
        
        # Timestamps
        created_at = mapped_column(DateTime, default=datetime.utcnow)
        updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Register the mapping
    mapping_registry.map_imperatively(
        Subscription,
        SubscriptionsTable,
        properties={
            "id": mapping_registry.column_property(
                SubscriptionsTable.id,
                SubscriptionId
            ),
            "name": mapping_registry.column_property(
                SubscriptionsTable.name,
                SubscriptionName
            ),
            "price": mapping_registry.column_property(
                SubscriptionsTable.price,
                Price
            ),
            "subscription_type": mapping_registry.column_property(
                SubscriptionsTable.subscription_type,
                SubscriptionType
            ),
            "currency": mapping_registry.column_property(
                SubscriptionsTable.currency,
                Currency
            ),
            "duration": mapping_registry.column_property(
                SubscriptionsTable.duration,
                Duration
            ),
            "features": mapping_registry.column_property(
                SubscriptionsTable.features,
                Features
            ),
            "is_active": mapping_registry.column_property(
                SubscriptionsTable.is_active,
                SubscriptionStatus
            ),
            "stripe_price_id": mapping_registry.column_property(
                SubscriptionsTable.stripe_price_id,
                StripePriceId
            ),
            "stripe_product_id": mapping_registry.column_property(
                SubscriptionsTable.stripe_product_id,
                StripeProductId
            ),
            "created_at": mapping_registry.column_property(
                SubscriptionsTable.created_at,
                CreatedAt
            ),
            "updated_at": mapping_registry.column_property(
                SubscriptionsTable.updated_at,
                UpdatedAt
            ),
        }
    )
