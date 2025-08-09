from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from app.application.common.ports.session_recorder import SessionRecorder
from app.infrastructure.adapters.types import MainAsyncSession
from app.infrastructure.exceptions.gateway import DataMapperError
from app.infrastructure.adapters.constants import DB_QUERY_FAILED
from app.infrastructure.persistence_sqla.mappings.session import map_sessions_table


class SqlaSessionRecorder(SessionRecorder):
    def __init__(self, session: MainAsyncSession):
        # ensure table is mapped
        map_sessions_table()
        self._session = session

    async def add(
        self,
        *,
        user_id: int,
        access_token: str,
        refresh_token: str,
        token_type: str,
        ip_address: str | None,
        user_agent: str | None,
        created_at: datetime,
        expires_at: datetime,
        last_activity: datetime,
        is_active: bool,
    ) -> None:
        try:
            # Use raw SQL to insert into sessions table to avoid ORM entity
            await self._session.execute(
                # nosec - values are bound parameters via SQLA
                """
                INSERT INTO sessions (
                    user_id, access_token, refresh_token, token_type,
                    ip_address, user_agent, created_at, expires_at,
                    last_activity, is_active
                ) VALUES (
                    :user_id, :access_token, :refresh_token, :token_type,
                    :ip_address, :user_agent, :created_at, :expires_at,
                    :last_activity, :is_active
                )
                """,
                {
                    "user_id": user_id,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": token_type,
                    "ip_address": ip_address,
                    "user_agent": user_agent,
                    "created_at": created_at,
                    "expires_at": expires_at,
                    "last_activity": last_activity,
                    "is_active": is_active,
                },
            )
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error


