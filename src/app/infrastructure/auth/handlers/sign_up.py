import logging
from dataclasses import dataclass
from typing import TypedDict

from app.application.common.ports.flusher import Flusher
from app.application.common.ports.transaction_manager import TransactionManager
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.application.common.services.current_user import CurrentUserService
from app.domain.exceptions.user import EmailAlreadyExistsError
from app.domain.services.user import UserService
from app.domain.value_objects.raw_password.raw_password import RawPassword
from app.domain.value_objects.email import Email
from app.domain.value_objects.first_name import FirstName
from app.domain.value_objects.last_name import LastName
from app.domain.value_objects.language import Language
from app.infrastructure.auth.exceptions import (
    AlreadyAuthenticatedError,
    AuthenticationError,
)
from app.infrastructure.auth.handlers.constants import (
    AUTH_ALREADY_AUTHENTICATED,
)

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class SignUpRequest:
    email: str
    first_name: str
    last_name: str
    password: str


class SignUpResponse(TypedDict):
    id: int


class SignUpHandler:
    """
    - Open to everyone.
    - Registers a new user with validation and uniqueness checks.
    - Passwords are peppered, salted, and stored as hashes.
    - A logged-in user cannot sign up until the session expires or is terminated.
    """

    def __init__(
        self,
        current_user_service: CurrentUserService,
        user_service: UserService,
        user_command_gateway: UserCommandGateway,
        flusher: Flusher,
        transaction_manager: TransactionManager,
    ):
        self._current_user_service = current_user_service
        self._user_service = user_service
        self._user_command_gateway = user_command_gateway
        self._flusher = flusher
        self._transaction_manager = transaction_manager

    async def execute(self, request_data: SignUpRequest) -> SignUpResponse:
        """
        :raises AlreadyAuthenticatedError:
        :raises AuthorizationError:
        :raises DataMapperError:
        :raises DomainFieldError:
        :raises RoleAssignmentNotPermittedError:
        :raises EmailAlreadyExistsError:
        """
        log.info("Sign up: started. Email: '%s'.", request_data.email)

        try:
            await self._current_user_service.get_current_user()
            raise AlreadyAuthenticatedError(AUTH_ALREADY_AUTHENTICATED)
        except AuthenticationError:
            pass

        email = Email(request_data.email)
        first_name = FirstName(request_data.first_name)
        last_name = LastName(request_data.last_name)
        password = RawPassword(request_data.password)
        language = Language("en")

        user = self._user_service.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            language=language,
        )

        self._user_command_gateway.add(user)

        try:
            await self._flusher.flush()
        except EmailAlreadyExistsError:
            raise

        await self._transaction_manager.commit()

        log.info("Sign up: done. Email: '%s'.", user.email.value)
        return SignUpResponse(id=user.id.value)
