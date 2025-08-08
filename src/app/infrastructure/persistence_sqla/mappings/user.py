"""
SQLAlchemy mapping for User entity.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum, ForeignKey
from sqlalchemy.orm import mapped_column
import sqlalchemy as sa

from app.domain.entities.user import User
from app.domain.enums.user_role import UserRole
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.email import Email
from app.domain.value_objects.first_name import FirstName
from app.domain.value_objects.last_name import LastName
from app.domain.value_objects.user_password_hash import UserPasswordHash
from app.domain.value_objects.user_status import UserActive, UserBlocked, UserVerified
from app.domain.value_objects.retry_count import RetryCount
from app.domain.value_objects.last_login import LastLogin
from app.domain.value_objects.profile_picture import ProfilePicture
from app.domain.value_objects.phone_number import PhoneNumber
from app.domain.value_objects.language import Language
from app.domain.value_objects.address import Address
from app.domain.value_objects.postal_code import PostalCode
from app.domain.value_objects.country_id import CountryId
from app.domain.value_objects.city_id import CityId
from app.domain.value_objects.subscription import Subscription
from app.domain.value_objects.created_at import CreatedAt
from app.domain.value_objects.updated_at import UpdatedAt
from app.infrastructure.persistence_sqla.registry import mapping_registry


def map_users_table() -> None:
    """Map User entity to database table."""
    
    @mapping_registry.mapped
    class UsersTable:
        __tablename__ = "users"
        
        # Primary key
        id = mapped_column(Integer, primary_key=True, index=True)
        
        # User information
        email = mapped_column(String(255), unique=True, index=True, nullable=False)
        first_name = mapped_column(String(100), nullable=False)
        last_name = mapped_column(String(100), nullable=False)
        role = mapped_column(Enum(UserRole, values_callable=lambda x: [e.value for e in x]), default=UserRole.USER)
        is_active = mapped_column(Boolean, default=True)
        is_blocked = mapped_column(Boolean, default=False)
        is_verified = mapped_column(Boolean, default=False)
        retry_count = mapped_column(Integer, default=0)
        password = mapped_column(String(255), nullable=False)
        
        # Timestamps
        created_at = mapped_column(DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
        updated_at = mapped_column(DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP'))
        last_login = mapped_column(DateTime, nullable=True)
        
        # Profile information
        profile_picture = mapped_column(String(255), nullable=True)
        phone_number = mapped_column(String(20), nullable=True)
        language = mapped_column(String(10), default="en")
        address = mapped_column(Text, nullable=True)
        postal_code = mapped_column(String(20), nullable=True)
        
        # Foreign keys
        country_id = mapped_column(Integer, ForeignKey("countries.id"), nullable=True)
        city_id = mapped_column(Integer, ForeignKey("cities.id"), nullable=True)
        
        # Subscription
        subscription = mapped_column(String(50), nullable=True)
    
    # Register the mapping
    mapping_registry.map_imperatively(
        User,
        UsersTable,
        properties={
            "id": mapping_registry.column_property(
                UsersTable.id,
                UserId
            ),
            "email": mapping_registry.column_property(
                UsersTable.email,
                Email
            ),
            "first_name": mapping_registry.column_property(
                UsersTable.first_name,
                FirstName
            ),
            "last_name": mapping_registry.column_property(
                UsersTable.last_name,
                LastName
            ),
            "role": UsersTable.role,
            "is_active": mapping_registry.column_property(
                UsersTable.is_active,
                UserActive
            ),
            "is_blocked": mapping_registry.column_property(
                UsersTable.is_blocked,
                UserBlocked
            ),
            "is_verified": mapping_registry.column_property(
                UsersTable.is_verified,
                UserVerified
            ),
            "retry_count": mapping_registry.column_property(
                UsersTable.retry_count,
                RetryCount
            ),
            "password": mapping_registry.column_property(
                UsersTable.password,
                UserPasswordHash
            ),
            "created_at": mapping_registry.column_property(
                UsersTable.created_at,
                CreatedAt
            ),
            "updated_at": mapping_registry.column_property(
                UsersTable.updated_at,
                UpdatedAt
            ),
            "last_login": mapping_registry.column_property(
                UsersTable.last_login,
                LastLogin
            ),
            "profile_picture": mapping_registry.column_property(
                UsersTable.profile_picture,
                ProfilePicture
            ),
            "phone_number": mapping_registry.column_property(
                UsersTable.phone_number,
                PhoneNumber
            ),
            "language": mapping_registry.column_property(
                UsersTable.language,
                Language
            ),
            "address": mapping_registry.column_property(
                UsersTable.address,
                Address
            ),
            "postal_code": mapping_registry.column_property(
                UsersTable.postal_code,
                PostalCode
            ),
            "country_id": mapping_registry.column_property(
                UsersTable.country_id,
                CountryId
            ),
            "city_id": mapping_registry.column_property(
                UsersTable.city_id,
                CityId
            ),
            "subscription": mapping_registry.column_property(
                UsersTable.subscription,
                Subscription
            ),
        }
    )
