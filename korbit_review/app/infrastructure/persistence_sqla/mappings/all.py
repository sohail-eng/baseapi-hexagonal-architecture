"""
Ensures imperative SQLAlchemy mappings are initialized at application startup.

### Purpose:
In Clean Architecture, domain entities remain agnostic of database
mappings. To integrate with SQLAlchemy, mappings must be explicitly
triggered to link ORM attributes to domain classes. Without this setup,
attempts to interact with unmapped entities in database operations
will lead to runtime errors.

### Solution:
This module provides a single entry point to initialize the mapping
of domain entities to database tables. By calling the `map_tables` function,
ORM attributes are linked to domain classes without altering domain code
or introducing infrastructure concerns.

### Usage:
Call the `map_tables` function in the application factory to initialize
mappings at startup. Additionally, it is necessary to call this function
in `env.py` for Alembic migrations to ensure all models are available
during database migrations.
"""

from app.infrastructure.persistence_sqla.mappings.auth_session import (
    map_auth_sessions_table,
)
from app.infrastructure.persistence_sqla.mappings.city import map_cities_table
from app.infrastructure.persistence_sqla.mappings.country import map_countries_table
from app.infrastructure.persistence_sqla.mappings.email_verification import map_email_verifications_table
from app.infrastructure.persistence_sqla.mappings.notification import map_notifications_table
from app.infrastructure.persistence_sqla.mappings.password_reset import map_password_resets_table
from app.infrastructure.persistence_sqla.mappings.payment import map_payments_table
from app.infrastructure.persistence_sqla.mappings.session import map_sessions_table
from app.infrastructure.persistence_sqla.mappings.subscription import map_subscriptions_table
from app.infrastructure.persistence_sqla.mappings.subscription_user import map_subscription_users_table
from app.infrastructure.persistence_sqla.mappings.user import map_users_table


def map_tables() -> None:
    map_users_table()
    map_auth_sessions_table()
    map_countries_table()
    map_cities_table()
    map_email_verifications_table()
    map_notifications_table()
    map_password_resets_table()
    map_payments_table()
    map_sessions_table()
    map_subscriptions_table()
    map_subscription_users_table()
