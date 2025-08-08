"""
SQLAlchemy mapping for Notification entity.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import mapped_column

from app.domain.entities.notification import Notification
from app.domain.value_objects.notification_id import NotificationId
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.notification_title import NotificationTitle
from app.domain.value_objects.notification_action import NotificationAction
from app.domain.value_objects.notification_data import NotificationData
from app.domain.value_objects.read_status import ReadStatus
from app.domain.value_objects.created_at import CreatedAt
from app.domain.value_objects.updated_at import UpdatedAt
from app.infrastructure.persistence_sqla.registry import mapping_registry


def map_notifications_table() -> None:
    """Map Notification entity to database table."""
    
    @mapping_registry.mapped
    class NotificationsTable:
        __tablename__ = "notifications"
        
        # Primary key
        id = mapped_column(Integer, primary_key=True, index=True)
        
        # Foreign key to users table
        user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
        
        # Notification information
        title = mapped_column(String(255), nullable=False)
        is_read = mapped_column(Boolean, default=False)
        action = mapped_column(String(50), nullable=False)  # e.g., 'payment', 'subscription', 'system'
        data_json = mapped_column(JSON, nullable=True)
        
        # Timestamps
        created_at = mapped_column(DateTime, default=datetime.utcnow)
        updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Register the mapping
    mapping_registry.map_imperatively(
        Notification,
        NotificationsTable,
        properties={
            "id": mapping_registry.column_property(
                NotificationsTable.id,
                NotificationId
            ),
            "user_id": mapping_registry.column_property(
                NotificationsTable.user_id,
                UserId
            ),
            "title": mapping_registry.column_property(
                NotificationsTable.title,
                NotificationTitle
            ),
            "is_read": mapping_registry.column_property(
                NotificationsTable.is_read,
                ReadStatus
            ),
            "action": mapping_registry.column_property(
                NotificationsTable.action,
                NotificationAction
            ),
            "data_json": mapping_registry.column_property(
                NotificationsTable.data_json,
                NotificationData
            ),
            "created_at": mapping_registry.column_property(
                NotificationsTable.created_at,
                CreatedAt
            ),
            "updated_at": mapping_registry.column_property(
                NotificationsTable.updated_at,
                UpdatedAt
            ),
        }
    )
