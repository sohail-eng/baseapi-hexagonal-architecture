"""
SQLAlchemy mapping for PasswordReset entity.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, text
from sqlalchemy.orm import mapped_column

from app.domain.entities.password_reset import PasswordReset
from app.domain.value_objects.password_reset_id import PasswordResetId
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.reset_token import ResetToken
from app.domain.value_objects.expiration_time import ExpirationTime
from app.domain.value_objects.reset_status import ResetStatus
from app.domain.value_objects.created_at import CreatedAt
from app.domain.value_objects.updated_at import UpdatedAt
from app.infrastructure.persistence_sqla.registry import mapping_registry


def map_password_resets_table() -> None:
    """Map PasswordReset entity to database table."""
    
    @mapping_registry.mapped
    class PasswordResetsTable:
        __tablename__ = "password_resets"
        
        # Primary key
        id = mapped_column(Integer, primary_key=True, index=True)
        
        # Foreign key to users table
        user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
        
        # Reset information
        token = mapped_column(String(255), nullable=False)
        expires_at = mapped_column(DateTime(timezone=True), nullable=False)
        is_used = mapped_column(Boolean, default=False)
        
        # Timestamps
        created_at = mapped_column(
            DateTime(timezone=True), 
            server_default=text('CURRENT_TIMESTAMP')
        )
        updated_at = mapped_column(
            DateTime(timezone=True), 
            server_default=text('CURRENT_TIMESTAMP'), 
            onupdate=text('CURRENT_TIMESTAMP')
        )
    
    # Register the mapping
    mapping_registry.map_imperatively(
        PasswordReset,
        PasswordResetsTable,
        properties={
            "id": mapping_registry.column_property(
                PasswordResetsTable.id,
                PasswordResetId
            ),
            "user_id": mapping_registry.column_property(
                PasswordResetsTable.user_id,
                UserId
            ),
            "token": mapping_registry.column_property(
                PasswordResetsTable.token,
                ResetToken
            ),
            "expires_at": mapping_registry.column_property(
                PasswordResetsTable.expires_at,
                ExpirationTime
            ),
            "is_used": mapping_registry.column_property(
                PasswordResetsTable.is_used,
                ResetStatus
            ),
            "created_at": mapping_registry.column_property(
                PasswordResetsTable.created_at,
                CreatedAt
            ),
            "updated_at": mapping_registry.column_property(
                PasswordResetsTable.updated_at,
                UpdatedAt
            ),
        }
    )
