from inspect import getdoc

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from fastapi_error_map import ErrorAwareRouter, rule
from pydantic import BaseModel, ConfigDict, Field

from app.application.commands.user.create_user import (
    CreateUserInteractor,
    CreateUserRequest,
    CreateUserResponse,
)
from app.application.common.exceptions.authorization import AuthorizationError
from app.domain.enums.user_role import UserRole
from app.domain.exceptions.base import DomainFieldError
from app.domain.exceptions.user import (
    RoleAssignmentNotPermittedError,
    EmailAlreadyExistsError,
)
from app.infrastructure.auth.exceptions import AuthenticationError
from app.infrastructure.exceptions.gateway import DataMapperError
from app.presentation.http.errors.callbacks import log_error, log_info
from app.presentation.http.errors.translators import (
    ServiceUnavailableTranslator,
)


class CreateUserRequestPydantic(BaseModel):
    """
    Using a Pydantic model here is generally unnecessary.
    It's only implemented to render a specific Swagger UI (OpenAPI) schema.
    """

    model_config = ConfigDict(frozen=True)

    email: str
    first_name: str
    last_name: str
    password: str
    role: UserRole = Field(default=UserRole.USER)


def create_create_user_router() -> APIRouter:
    router = ErrorAwareRouter()

    @router.post(
        "/",
        description=getdoc(CreateUserInteractor),
        error_map={
            AuthenticationError: status.HTTP_401_UNAUTHORIZED,
            DataMapperError: rule(
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
                translator=ServiceUnavailableTranslator(),
                on_error=log_error,
            ),
            AuthorizationError: status.HTTP_403_FORBIDDEN,
            DomainFieldError: status.HTTP_400_BAD_REQUEST,
            RoleAssignmentNotPermittedError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            EmailAlreadyExistsError: status.HTTP_409_CONFLICT,
        },
        default_on_error=log_info,
        status_code=status.HTTP_201_CREATED,
    )
    @inject
    async def create_user(
        request_data_pydantic: CreateUserRequestPydantic,
        interactor: FromDishka[CreateUserInteractor],
    ) -> CreateUserResponse:
        request_data = CreateUserRequest(
            email=request_data_pydantic.email,
            first_name=request_data_pydantic.first_name,
            last_name=request_data_pydantic.last_name,
            password=request_data_pydantic.password,
            role=request_data_pydantic.role,
        )
        return await interactor.execute(request_data)

    return router
