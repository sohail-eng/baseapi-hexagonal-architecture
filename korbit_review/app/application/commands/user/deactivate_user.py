import logging
from dataclasses import dataclass

from app.application.common.ports.access_revoker import AccessRevoker
from app.application.common.ports.transaction_manager import (
    TransactionManager,
)
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.application.common.services.authorization.authorize import (
    authorize,
)
from app.application.common.services.authorization.permissions import (
    CanManageRole,
    CanManageSubordinate,
    RoleManagementContext,
    UserManagementContext,
)
from app.application.common.services.current_user import CurrentUserService
from app.domain.entities.user import User
from app.domain.enums.user_role import UserRole
from app.domain.exceptions.user import UserNotFoundByEmailError
from app.domain.services.user import UserService
from app.domain.value_objects.email import Email

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class DeactivateUserRequest:
    email: str


class DeactivateUserInteractor:
    """
    - Open to admins.
    - Soft-deletes an existing user, making that user inactive.
    - Also deletes the user's sessions.
    - Only admins can deactivate other admins.
    - Admins cannot be soft-deleted by subordinates.
    """

    def __init__(
        self,
        current_user_service: CurrentUserService,
        user_command_gateway: UserCommandGateway,
        user_service: UserService,
        transaction_manager: TransactionManager,
        access_revoker: AccessRevoker,
    ):
        self._current_user_service = current_user_service
        self._user_command_gateway = user_command_gateway
        self._user_service = user_service
        self._transaction_manager = transaction_manager
        self._access_revoker = access_revoker

    async def execute(self, request_data: DeactivateUserRequest) -> None:
        """
        :raises AuthenticationError:
        :raises DataMapperError:
        :raises AuthorizationError:
        :raises DomainFieldError:
        :raises UserNotFoundByEmailError:
        :raises ActivationChangeNotPermittedError:
        """
        log.info(
            "Deactivate user: started. Email: '%s'.",
            request_data.email,
        )

        current_user = await self._current_user_service.get_current_user()

        authorize(
            CanManageRole(),
            context=RoleManagementContext(
                subject=current_user,
                target_role=UserRole.USER,
            ),
        )

        email = Email(request_data.email)
        user: User | None = await self._user_command_gateway.read_by_email(
            email,
            for_update=True,
        )
        if user is None:
            raise UserNotFoundByEmailError(email)

        authorize(
            CanManageSubordinate(),
            context=UserManagementContext(
                subject=current_user,
                target=user,
            ),
        )

        self._user_service.toggle_user_activation(user, is_active=False)
        await self._transaction_manager.commit()
        await self._access_revoker.remove_all_user_access(user.id_)

        log.info(
            "Deactivate user: done. Email: '%s'.",
            user.email.value,
        )
