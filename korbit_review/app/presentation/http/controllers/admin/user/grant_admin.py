from inspect import getdoc
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Path, Security, status
from fastapi_error_map import ErrorAwareRouter, rule

from app.application.commands.user.grant_admin import (
    GrantAdminInteractor,
    GrantAdminRequest,
)
from app.application.common.exceptions.authorization import AuthorizationError
from app.domain.exceptions.base import DomainFieldError
from app.domain.exceptions.user import (
    RoleChangeNotPermittedError,
    UserNotFoundByEmailError,
)
from app.infrastructure.auth.exceptions import AuthenticationError
from app.infrastructure.exceptions.gateway import DataMapperError
from app.presentation.http.auth.fastapi_openapi_markers import bearer_scheme
from app.presentation.http.errors.callbacks import log_error, log_info
from app.presentation.http.errors.translators import (
    ServiceUnavailableTranslator,
)


def create_grant_admin_router() -> APIRouter:
    router = ErrorAwareRouter()

    @router.patch(
        "/{email}/grant-admin",
        description=getdoc(GrantAdminInteractor),
        error_map={
            AuthenticationError: status.HTTP_401_UNAUTHORIZED,
            DataMapperError: rule(
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
                translator=ServiceUnavailableTranslator(),
                on_error=log_error,
            ),
            AuthorizationError: status.HTTP_403_FORBIDDEN,
            DomainFieldError: status.HTTP_400_BAD_REQUEST,
            UserNotFoundByEmailError: status.HTTP_404_NOT_FOUND,
            RoleChangeNotPermittedError: status.HTTP_403_FORBIDDEN,
        },
        default_on_error=log_info,
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Security(bearer_scheme)],
    )
    @inject
    async def grant_admin(
        email: Annotated[str, Path()],
        interactor: FromDishka[GrantAdminInteractor],
    ) -> None:
        request_data = GrantAdminRequest(email)
        await interactor.execute(request_data)

    return router
