import logging
from dataclasses import dataclass
from typing import TypedDict, Optional
from uuid import UUID

from app.application.common.ports.flusher import Flusher
from app.application.common.ports.transaction_manager import (
    TransactionManager,
)
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.application.common.services.authorization.authorize import (
    authorize,
)
from app.application.common.services.authorization.permissions import (
    CanManageRole,
    RoleManagementContext,
)
from app.application.common.services.current_user import CurrentUserService
from app.domain.enums.user_role import UserRole
from app.domain.exceptions.user import EmailAlreadyExistsError
from app.domain.services.user import UserService
from app.domain.value_objects.raw_password.raw_password import RawPassword
from app.domain.value_objects.email import Email
from app.domain.value_objects.first_name import FirstName
from app.domain.value_objects.last_name import LastName
from app.domain.value_objects.phone_number import PhoneNumber
from app.domain.value_objects.language import Language
from app.domain.value_objects.address import Address
from app.domain.value_objects.postal_code import PostalCode
from app.domain.value_objects.country_id import CountryId
from app.domain.value_objects.city_id import CityId
from app.domain.value_objects.subscription import Subscription

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserRequest:
    email: str
    first_name: str
    last_name: str
    password: str
    role: UserRole
    phone_number: Optional[str] = None
    language: str = "en"
    address: Optional[str] = None
    postal_code: Optional[str] = None
    country_id: Optional[int] = None
    city_id: Optional[int] = None
    subscription: Optional[str] = None


class CreateUserResponse(TypedDict):
    id: UUID


class CreateUserInteractor:
    """
    - Open to admins.
    - Creates a new user, including admins, if the email is unique.
    - Only admins can create new admins.
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

    async def execute(self, request_data: CreateUserRequest) -> CreateUserResponse:
        """
        :raises AuthenticationError:
        :raises DataMapperError:
        :raises AuthorizationError:
        :raises DomainFieldError:
        :raises RoleAssignmentNotPermittedError:
        :raises EmailAlreadyExistsError:
        """
        log.info(
            "Create user: started. Email: '%s'.",
            request_data.email,
        )

        current_user = await self._current_user_service.get_current_user()

        authorize(
            CanManageRole(),
            context=RoleManagementContext(
                subject=current_user,
                target_role=request_data.role,
            ),
        )

        email = Email(request_data.email)
        first_name = FirstName(request_data.first_name)
        last_name = LastName(request_data.last_name)
        password = RawPassword(request_data.password)
        
        # Optional fields
        phone_number = PhoneNumber(request_data.phone_number) if request_data.phone_number else None
        language = Language(request_data.language)
        address = Address(request_data.address) if request_data.address else None
        postal_code = PostalCode(request_data.postal_code) if request_data.postal_code else None
        country_id = CountryId(request_data.country_id) if request_data.country_id else None
        city_id = CityId(request_data.city_id) if request_data.city_id else None
        subscription = Subscription(request_data.subscription) if request_data.subscription else None
        
        user = self._user_service.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=request_data.role,
            phone_number=phone_number,
            language=language,
            address=address,
            postal_code=postal_code,
            country_id=country_id,
            city_id=city_id,
            subscription=subscription,
        )

        self._user_command_gateway.add(user)

        try:
            await self._flusher.flush()
        except EmailAlreadyExistsError:
            raise

        await self._transaction_manager.commit()

        log.info("Create user: done. Email: '%s'.", user.email.value)
        return CreateUserResponse(id=user.id.value)
