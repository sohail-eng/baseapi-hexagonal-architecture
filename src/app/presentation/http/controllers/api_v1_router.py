from fastapi import APIRouter

from app.presentation.http.controllers.account.router import create_account_router
from app.presentation.http.controllers.general.router import create_general_router
from app.presentation.http.controllers.users.router import create_users_router
from app.presentation.http.controllers.atlas.router import create_atlas_router


def create_api_v1_router() -> APIRouter:
    router = APIRouter(
        prefix="/api/v1",
    )

    sub_routers = (
        create_account_router(),
        create_general_router(),
        create_users_router(),
        create_atlas_router(),
    )

    for sub_router in sub_routers:
        router.include_router(sub_router)

    return router
