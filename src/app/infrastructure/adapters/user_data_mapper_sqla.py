from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.domain.entities.user import User
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.email import Email
from app.infrastructure.adapters.constants import DB_QUERY_FAILED, DB_CONSTRAINT_VIOLATION
from app.infrastructure.adapters.types import MainAsyncSession
from app.infrastructure.exceptions.gateway import DataMapperError
from app.infrastructure.persistence_sqla.mappings.user import map_users_table
from app.infrastructure.persistence_sqla.registry import mapping_registry
from app.domain.exceptions.user import EmailAlreadyExistsError


class SqlaUserDataMapper(UserCommandGateway):
    def __init__(self, session: MainAsyncSession):
        self._session = session

    async def add(self, user: User) -> None:
        """
        :raises DataMapperError:
        """
        try:
            # Insert explicitly into users table and set generated id on domain entity
            map_users_table()
            UsersTable = mapping_registry.metadata.tables["users"]  # type: ignore
            values = {
                "email": user.email.value,
                "first_name": user.first_name.value,
                "last_name": user.last_name.value,
                "role": user.role.value,
                "is_active": user.is_active.value,
                "is_blocked": user.is_blocked.value,
                "is_verified": user.is_verified.value,
                "retry_count": user.retry_count.value,
                # store password hash as bytes/blob or decoded string depending on schema
                "password": user.password.value.decode("utf-8", errors="ignore"),
                "profile_picture": user.profile_picture.value if user.profile_picture else None,
                "phone_number": user.phone_number.value if user.phone_number else None,
                "language": user.language.value,
                "address": user.address.value if user.address else None,
                "postal_code": user.postal_code.value if user.postal_code else None,
                "country_id": user.country_id.value if user.country_id else None,
                "city_id": user.city_id.value if user.city_id else None,
                "subscription": user.subscription.value if user.subscription else None,
            }
            insert_stmt = UsersTable.insert().values(**values).returning(UsersTable.c.id)
            result = await self._session.execute(insert_stmt)
            new_id = result.scalar_one()
            # Assign generated id back to domain entity if placeholder
            if getattr(user.id_, "value", None) in (None, 0):
                user.id_ = UserId(new_id)

        except IntegrityError as error:
            if "email" in str(error).lower():
                raise EmailAlreadyExistsError(user.email.value) from error
            raise DataMapperError(DB_CONSTRAINT_VIOLATION) from error
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error

    async def read_by_id(self, user_id: UserId) -> User | None:
        """
        :raises DataMapperError:
        """
        select_stmt: Select[tuple[User]] = select(User).where(User.id == user_id)  # type: ignore

        try:
            user: User | None = (
                await self._session.execute(select_stmt)
            ).scalar_one_or_none()

            return user

        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error

    async def read_by_email(
        self,
        email: Email,
        for_update: bool = False,
    ) -> User | None:
        """
        :raises DataMapperError:
        """
        select_stmt: Select[tuple[User]] = select(User).where(User.email == email)  # type: ignore

        if for_update:
            select_stmt = select_stmt.with_for_update()

        try:
            user: User | None = (
                await self._session.execute(select_stmt)
            ).scalar_one_or_none()

            return user

        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error
