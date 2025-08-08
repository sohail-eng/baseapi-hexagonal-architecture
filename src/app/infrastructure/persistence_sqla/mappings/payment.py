"""
SQLAlchemy mapping for Payment entity.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import mapped_column

from app.domain.entities.payment import Payment
from app.domain.value_objects.payment_id import PaymentId
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.subscription_id import SubscriptionId
from app.domain.value_objects.subscription_user_id import SubscriptionUserId
from app.domain.value_objects.amount import Amount
from app.domain.value_objects.currency import Currency
from app.domain.value_objects.payment_status import PaymentStatus
from app.domain.value_objects.stripe_payment_intent_id import StripePaymentIntentId
from app.domain.value_objects.stripe_customer_id import StripeCustomerId
from app.domain.value_objects.payment_data import PaymentData
from app.domain.value_objects.payment_method import PaymentMethod
from app.domain.value_objects.payment_type import PaymentType
from app.domain.value_objects.payment_date import PaymentDate
from app.domain.value_objects.data_json import DataJson
from app.domain.value_objects.created_at import CreatedAt
from app.domain.value_objects.updated_at import UpdatedAt
from app.infrastructure.persistence_sqla.registry import mapping_registry


def map_payments_table() -> None:
    """Map Payment entity to database table."""
    
    @mapping_registry.mapped
    class PaymentsTable:
        __tablename__ = "payments"
        
        # Primary key
        id = mapped_column(Integer, primary_key=True, index=True)
        
        # Foreign keys
        user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
        subscription_id = mapped_column(Integer, ForeignKey("subscriptions.id", ondelete="SET NULL"), nullable=True)
        subscription_user_id = mapped_column(Integer, ForeignKey("subscription_users.id", ondelete="SET NULL"), nullable=True)
        
        # Payment information
        amount = mapped_column(Float, nullable=True)
        currency = mapped_column(String(3), default="USD")
        status = mapped_column(String(50), nullable=False, default="pending")
        stripe_payment_intent_id = mapped_column(String(255), nullable=True)
        stripe_customer_id = mapped_column(String(255), nullable=True)
        payment_data = mapped_column(JSON, nullable=True)
        payment_method = mapped_column(String(50), nullable=True)
        payment_type = mapped_column(String(50), nullable=True)
        date = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
        data_json = mapped_column(JSON, nullable=True)
        
        # Timestamps
        created_at = mapped_column(DateTime, default=datetime.utcnow)
        updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Register the mapping
    mapping_registry.map_imperatively(
        Payment,
        PaymentsTable,
        properties={
            "id": mapping_registry.column_property(
                PaymentsTable.id,
                PaymentId
            ),
            "user_id": mapping_registry.column_property(
                PaymentsTable.user_id,
                UserId
            ),
            "subscription_id": mapping_registry.column_property(
                PaymentsTable.subscription_id,
                SubscriptionId
            ),
            "subscription_user_id": mapping_registry.column_property(
                PaymentsTable.subscription_user_id,
                SubscriptionUserId
            ),
            "amount": mapping_registry.column_property(
                PaymentsTable.amount,
                Amount
            ),
            "currency": mapping_registry.column_property(
                PaymentsTable.currency,
                Currency
            ),
            "status": mapping_registry.column_property(
                PaymentsTable.status,
                PaymentStatus
            ),
            "stripe_payment_intent_id": mapping_registry.column_property(
                PaymentsTable.stripe_payment_intent_id,
                StripePaymentIntentId
            ),
            "stripe_customer_id": mapping_registry.column_property(
                PaymentsTable.stripe_customer_id,
                StripeCustomerId
            ),
            "payment_data": mapping_registry.column_property(
                PaymentsTable.payment_data,
                PaymentData
            ),
            "payment_method": mapping_registry.column_property(
                PaymentsTable.payment_method,
                PaymentMethod
            ),
            "payment_type": mapping_registry.column_property(
                PaymentsTable.payment_type,
                PaymentType
            ),
            "date": mapping_registry.column_property(
                PaymentsTable.date,
                PaymentDate
            ),
            "data_json": mapping_registry.column_property(
                PaymentsTable.data_json,
                DataJson
            ),
            "created_at": mapping_registry.column_property(
                PaymentsTable.created_at,
                CreatedAt
            ),
            "updated_at": mapping_registry.column_property(
                PaymentsTable.updated_at,
                UpdatedAt
            ),
        }
    )
