"""
SQLAlchemy mapping for Session entity.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column

from app.domain.entities.session import Session
from app.domain.value_objects.session_id import SessionId
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.access_token import AccessToken
from app.domain.value_objects.refresh_token import RefreshToken
from app.domain.value_objects.token_type import TokenType
from app.domain.value_objects.ip_address import IpAddress
from app.domain.value_objects.user_agent import UserAgent
from app.domain.value_objects.expiration_time import ExpirationTime
from app.domain.value_objects.last_activity import LastActivity
from app.domain.value_objects.session_status import SessionStatus
from app.domain.value_objects.created_at import CreatedAt
from app.infrastructure.persistence_sqla.registry import mapping_registry


def map_sessions_table() -> None:
    """Map Session entity to database table."""
    
    @mapping_registry.mapped
    class SessionsTable:
        __tablename__ = "sessions"
        
        # Primary key
        id = mapped_column(Integer, primary_key=True, index=True)
        
        # Foreign key to users table
        user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
        
        # Session information
        access_token = mapped_column(String(500), nullable=False)
        refresh_token = mapped_column(String(500), nullable=False)
        token_type = mapped_column(String(50), default="bearer")
        ip_address = mapped_column(String(50), nullable=True)
        user_agent = mapped_column(String(500), nullable=True)
        
        # Timestamps
        created_at = mapped_column(DateTime, default=datetime.utcnow)
        expires_at = mapped_column(DateTime, nullable=False)
        last_activity = mapped_column(DateTime, default=datetime.utcnow)
        is_active = mapped_column(Boolean, default=True)
    
    # Register the mapping
    mapping_registry.map_imperatively(
        Session,
        SessionsTable,
        properties={
            "id": mapping_registry.column_property(
                SessionsTable.id,
                SessionId
            ),
            "user_id": mapping_registry.column_property(
                SessionsTable.user_id,
                UserId
            ),
            "access_token": mapping_registry.column_property(
                SessionsTable.access_token,
                AccessToken
            ),
            "refresh_token": mapping_registry.column_property(
                SessionsTable.refresh_token,
                RefreshToken
            ),
            "token_type": mapping_registry.column_property(
                SessionsTable.token_type,
                TokenType
            ),
            "ip_address": mapping_registry.column_property(
                SessionsTable.ip_address,
                IpAddress
            ),
            "user_agent": mapping_registry.column_property(
                SessionsTable.user_agent,
                UserAgent
            ),
            "created_at": mapping_registry.column_property(
                SessionsTable.created_at,
                CreatedAt
            ),
            "expires_at": mapping_registry.column_property(
                SessionsTable.expires_at,
                ExpirationTime
            ),
            "last_activity": mapping_registry.column_property(
                SessionsTable.last_activity,
                LastActivity
            ),
            "is_active": mapping_registry.column_property(
                SessionsTable.is_active,
                SessionStatus
            ),
        }
    )
