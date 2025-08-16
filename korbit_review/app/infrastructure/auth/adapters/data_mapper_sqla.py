from sqlalchemy import Delete, delete
from sqlalchemy.exc import SQLAlchemyError

from app.domain.value_objects.user_id import UserId
from app.infrastructure.adapters.constants import DB_QUERY_FAILED
from app.infrastructure.auth.adapters.types import AuthAsyncSession
from app.infrastructure.auth.session.model import AuthSession
from app.infrastructure.auth.session.ports.gateway import (
    AuthSessionGateway,
)
from app.infrastructure.exceptions.gateway import DataMapperError


class SqlaAuthSessionDataMapper(AuthSessionGateway):
    def __init__(self, session: AuthAsyncSession):
        self._session = session

    def add(self, auth_session: AuthSession) -> None:
        """
        :raises DataMapperError:
        """
        try:
            self._session.add(auth_session)

        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error

    async def read_by_id(
        self,
        auth_session_id: str,
        for_update: bool = False,
    ) -> AuthSession | None:
        """
        :raises DataMapperError:
        """
        try:
            auth_session: AuthSession | None = await self._session.get(
                AuthSession,
                auth_session_id,
                with_for_update=for_update,
            )

            return auth_session

        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error

    async def update(self, auth_session: AuthSession) -> None:
        """
        :raises DataMapperError:
        """
        try:
            await self._session.merge(auth_session)

        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error

    async def delete(self, auth_session_id: str) -> None:
        """
        :raises DataMapperError:
        """
        delete_stmt: Delete = delete(AuthSession).where(
            AuthSession.id_ == auth_session_id,  # type: ignore
        )

        try:
            await self._session.execute(delete_stmt)

        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error

    async def delete_all_for_user(self, user_id: UserId) -> None:
        """
        :raises DataMapperError:
        """
        delete_stmt: Delete = delete(AuthSession).where(
            AuthSession.user_id == user_id,  # type: ignore
        )

        try:
            await self._session.execute(delete_stmt)

        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error
