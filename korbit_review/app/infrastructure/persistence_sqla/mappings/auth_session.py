from sqlalchemy import Column, DateTime, String, Table, Integer, ForeignKey
from sqlalchemy.orm import composite

from app.domain.value_objects.user_id import UserId
from app.infrastructure.auth.session.model import AuthSession
from app.infrastructure.persistence_sqla.registry import mapping_registry

auth_sessions_table = Table(
    "auth_sessions",
    mapping_registry.metadata,
    Column("id", String, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("expiration", DateTime(timezone=True), nullable=False),
)


def map_auth_sessions_table() -> None:
    mapping_registry.map_imperatively(
        AuthSession,
        auth_sessions_table,
        properties={
            "id_": auth_sessions_table.c.id,
            "user_id": composite(UserId, auth_sessions_table.c.user_id),
            "expiration": auth_sessions_table.c.expiration,
        },
        column_prefix="_",
    )
