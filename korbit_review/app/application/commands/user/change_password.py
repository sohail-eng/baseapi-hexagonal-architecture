import logging
from dataclasses import dataclass

from app.application.common.ports.transaction_manager import (
    TransactionManager,
)
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.application.common.services.authorization.authorize import (
    authorize,
)
from app.application.common.services.authorization.composite import AnyOf
from app.application.common.services.authorization.permissions import (
    CanManageSelf,
    CanManageSubordinate,
    UserManagementContext,
)
from app.application.common.services.current_user import CurrentUserService
from app.domain.entities.user import User
from app.domain.exceptions.user import UserNotFoundByEmailError
from app.domain.services.user import UserService
from app.domain.value_objects.raw_password.raw_password import RawPassword
from app.domain.value_objects.email import Email

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangePasswordRequest:
    email: str
    password: str


class ChangePasswordInteractor:
    """
    - Open to authenticated users.
    - Changes the user's password.
    - The current user can change their own password.
    - Admins can change passwords of subordinate users.
    """

    def __init__(
        self,
        current_user_service: CurrentUserService,
        user_command_gateway: UserCommandGateway,
        user_service: UserService,
        transaction_manager: TransactionManager,
    ):
        self._current_user_service = current_user_service
        self._user_command_gateway = user_command_gateway
        self._user_service = user_service
        self._transaction_manager = transaction_manager

    async def execute(self, request_data: ChangePasswordRequest) -> None:
        """
        :raises AuthenticationError:
        :raises DataMapperError:
        :raises AuthorizationError:
        :raises DomainFieldError:
        :raises UserNotFoundByEmailError:
        """
        log.info("Change password: started.")

        current_user = await self._current_user_service.get_current_user()

        email = Email(request_data.email)
        password = RawPassword(request_data.password)
        user: User | None = await self._user_command_gateway.read_by_email(
            email,
            for_update=True,
        )
        if user is None:
            raise UserNotFoundByEmailError(email)

        authorize(
            AnyOf(
                CanManageSelf(),
                CanManageSubordinate(),
            ),
            context=UserManagementContext(
                subject=current_user,
                target=user,
            ),
        )

        self._user_service.change_password(user, password)
        await self._transaction_manager.commit()

        log.info("Change password: done.")
