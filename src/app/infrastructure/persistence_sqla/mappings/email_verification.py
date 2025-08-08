"""
SQLAlchemy mapping for EmailVerification entity.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, text
from sqlalchemy.orm import mapped_column

from app.domain.entities.email_verification import EmailVerification
from app.domain.value_objects.email_verification_id import EmailVerificationId
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.verification_token import VerificationToken
from app.domain.value_objects.expiration_time import ExpirationTime
from app.domain.value_objects.verification_status import VerificationStatus
from app.domain.value_objects.created_at import CreatedAt
from app.domain.value_objects.updated_at import UpdatedAt
from app.infrastructure.persistence_sqla.registry import mapping_registry


def map_email_verifications_table() -> None:
    """Map EmailVerification entity to database table."""
    
    @mapping_registry.mapped
    class EmailVerificationsTable:
        __tablename__ = "email_verifications"
        
        # Primary key
        id = mapped_column(Integer, primary_key=True, index=True)
        
        # Foreign key to users table
        user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
        
        # Verification information
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
        EmailVerification,
        EmailVerificationsTable,
        properties={
            "id": mapping_registry.column_property(
                EmailVerificationsTable.id,
                EmailVerificationId
            ),
            "user_id": mapping_registry.column_property(
                EmailVerificationsTable.user_id,
                UserId
            ),
            "token": mapping_registry.column_property(
                EmailVerificationsTable.token,
                VerificationToken
            ),
            "expires_at": mapping_registry.column_property(
                EmailVerificationsTable.expires_at,
                ExpirationTime
            ),
            "is_used": mapping_registry.column_property(
                EmailVerificationsTable.is_used,
                VerificationStatus
            ),
            "created_at": mapping_registry.column_property(
                EmailVerificationsTable.created_at,
                CreatedAt
            ),
            "updated_at": mapping_registry.column_property(
                EmailVerificationsTable.updated_at,
                UpdatedAt
            ),
        }
    )
