import asyncio
from dishka import Scope
from dishka.async_container import enter_scope
from celery.schedules import crontab

from app.infrastructure.celery.app import celery_app
from app.setup.ioc.provider_registry import get_providers
from app.setup.ioc.application import ApplicationProvider
from app.setup.ioc.infrastructure import infrastructure_provider
from app.setup.ioc.presentation import PresentationProvider
from app.setup.ioc.settings import SettingsProvider
from app.setup.app_factory import create_async_ioc_container
from app.setup.config.settings import load_settings
from app.application.maintenance.tasks import (
    CleanupExpiredPasswordResetsTask,
    CleanupExpiredSessionsTask,
)


async def _run_task(coro_factory):
    settings = load_settings()
    container = create_async_ioc_container(
        providers=(
            ApplicationProvider(),
            infrastructure_provider(),
            PresentationProvider(),
            SettingsProvider(),
        ),
        settings=settings,
    )
    try:
        # Enter REQUEST scope so REQUEST-scoped providers (e.g., repositories, sessions) are available
        async with enter_scope(container, Scope.REQUEST):
            await coro_factory(container)
    finally:
        await container.close()


@celery_app.task(name="cleanup_expired_sessions")
def cleanup_expired_sessions():
    async def runner(container):
        repo = await container.get("app.application.maintenance.ports.AuthSessionRepository")  # type: ignore
        task = CleanupExpiredSessionsTask(repo)
        await task.run()

    asyncio.run(_run_task(runner))


@celery_app.task(name="cleanup_expired_password_resets")
def cleanup_expired_password_resets():
    async def runner(container):
        repo = await container.get("app.application.maintenance.ports.PasswordResetRepository")  # type: ignore
        task = CleanupExpiredPasswordResetsTask(repo)
        await task.run()

    asyncio.run(_run_task(runner))


celery_app.conf.beat_schedule = {
    "cleanup-expired-sessions": {
        "task": "cleanup_expired_sessions",
        "schedule": crontab(hour=0, minute=0),
    },
    "cleanup-expired-password-resets": {
        "task": "cleanup_expired_password_resets",
        "schedule": crontab(minute=0),
    },
}


