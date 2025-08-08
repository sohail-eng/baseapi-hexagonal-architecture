"""
SQLAlchemy mapping for SubscriptionUser entity.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import mapped_column

from app.domain.entities.subscription_user import SubscriptionUser
from app.domain.value_objects.subscription_user_id import SubscriptionUserId
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.subscription_id import SubscriptionId
from app.domain.value_objects.subscription_status import SubscriptionStatus
from app.domain.value_objects.start_date import StartDate
from app.domain.value_objects.end_date import EndDate
from app.domain.value_objects.stripe_subscription_id import StripeSubscriptionId
from app.domain.value_objects.stripe_customer_id import StripeCustomerId
from app.domain.value_objects.client_secret import ClientSecret
from app.domain.value_objects.subscription_data import SubscriptionData
from app.domain.value_objects.data_json import DataJson
from app.domain.value_objects.created_at import CreatedAt
from app.domain.value_objects.updated_at import UpdatedAt
from app.infrastructure.persistence_sqla.registry import mapping_registry


def map_subscription_users_table() -> None:
    """Map SubscriptionUser entity to database table."""
    
    @mapping_registry.mapped
    class SubscriptionUsersTable:
        __tablename__ = "subscription_users"
        
        # Primary key
        id = mapped_column(Integer, primary_key=True, index=True)
        
        # Foreign keys
        user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
        subscription_id = mapped_column(Integer, ForeignKey("subscriptions.id"), nullable=False)
        
        # Subscription user information
        status = mapped_column(String(50), nullable=False, default="pending")  # pending, cancelled, active
        start_date = mapped_column(DateTime(timezone=True), nullable=True)
        end_date = mapped_column(DateTime(timezone=True), nullable=True)
        stripe_subscription_id = mapped_column(String(255), nullable=True)
        stripe_customer_id = mapped_column(String(255), nullable=True)
        client_secret = mapped_column(String(255), nullable=True)
        subscription_data = mapped_column(JSON, nullable=True)
        data_json = mapped_column(JSON, nullable=True, default=dict)
        
        # Timestamps
        created_at = mapped_column(DateTime(timezone=True), server_default="now()")
        updated_at = mapped_column(DateTime(timezone=True), onupdate="now()")
    
    # Register the mapping
    mapping_registry.map_imperatively(
        SubscriptionUser,
        SubscriptionUsersTable,
        properties={
            "id": mapping_registry.column_property(
                SubscriptionUsersTable.id,
                SubscriptionUserId
            ),
            "user_id": mapping_registry.column_property(
                SubscriptionUsersTable.user_id,
                UserId
            ),
            "subscription_id": mapping_registry.column_property(
                SubscriptionUsersTable.subscription_id,
                SubscriptionId
            ),
            "status": mapping_registry.column_property(
                SubscriptionUsersTable.status,
                SubscriptionStatus
            ),
            "start_date": mapping_registry.column_property(
                SubscriptionUsersTable.start_date,
                StartDate
            ),
            "end_date": mapping_registry.column_property(
                SubscriptionUsersTable.end_date,
                EndDate
            ),
            "stripe_subscription_id": mapping_registry.column_property(
                SubscriptionUsersTable.stripe_subscription_id,
                StripeSubscriptionId
            ),
            "stripe_customer_id": mapping_registry.column_property(
                SubscriptionUsersTable.stripe_customer_id,
                StripeCustomerId
            ),
            "client_secret": mapping_registry.column_property(
                SubscriptionUsersTable.client_secret,
                ClientSecret
            ),
            "subscription_data": mapping_registry.column_property(
                SubscriptionUsersTable.subscription_data,
                SubscriptionData
            ),
            "data_json": mapping_registry.column_property(
                SubscriptionUsersTable.data_json,
                DataJson
            ),
            "created_at": mapping_registry.column_property(
                SubscriptionUsersTable.created_at,
                CreatedAt
            ),
            "updated_at": mapping_registry.column_property(
                SubscriptionUsersTable.updated_at,
                UpdatedAt
            ),
        }
    )
