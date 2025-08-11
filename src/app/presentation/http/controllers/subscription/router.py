from dataclasses import asdict
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Security, status
from fastapi_error_map import ErrorAwareRouter, rule

from app.infrastructure.subscription.handlers.get_subscriptions import (
    GetSubscriptionsHandler,
)
from app.infrastructure.subscription.handlers.init_subscriptions import (
    InitSubscriptionsHandler,
)
from app.infrastructure.exceptions.gateway import DataMapperError
from app.presentation.http.auth.fastapi_openapi_markers import bearer_scheme
from app.presentation.http.errors.callbacks import log_error, log_info
from app.presentation.http.errors.translators import ServiceUnavailableTranslator


def create_subscription_router() -> APIRouter:
    router = ErrorAwareRouter(prefix="/subscription", tags=["Subscription"])

    @router.get(
        "/",
        description="Get all available subscriptions",
        dependencies=[Security(bearer_scheme)],
        error_map={
            DataMapperError: rule(
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
                translator=ServiceUnavailableTranslator(),
                on_error=log_error,
            ),
        },
        default_on_error=log_info,
        status_code=status.HTTP_200_OK,
    )
    @inject
    async def get_subscriptions(
        handler: FromDishka[GetSubscriptionsHandler],
    ) -> list[dict]:
        items = await handler.execute()
        return [asdict(item) for item in items]

    @router.post(
        "/init",
        description="Initialize default subscriptions (PRO and CORPORATE).",
        dependencies=[Security(bearer_scheme)],
        error_map={
            DataMapperError: rule(
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
                translator=ServiceUnavailableTranslator(),
                on_error=log_error,
            ),
        },
        default_on_error=log_info,
        status_code=status.HTTP_200_OK,
    )
    @inject
    async def init_subscriptions(
        handler: FromDishka[InitSubscriptionsHandler],
    ) -> list[dict]:
        return await handler.execute(None)

    return router


