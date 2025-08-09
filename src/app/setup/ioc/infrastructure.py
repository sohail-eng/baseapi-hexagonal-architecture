from dishka import Provider, Scope, provide, provide_all

from app.infrastructure.adapters.main_transaction_manager_sqla import (
    SqlaMainTransactionManager,
)
from app.infrastructure.adapters.user_data_mapper_sqla import (
    SqlaUserDataMapper,
)
from app.infrastructure.adapters.user_reader_sqla import SqlaUserReader
from app.infrastructure.adapters.country_reader_sqla import SqlaCountryReader
from app.infrastructure.adapters.city_reader_sqla import SqlaCityReader
from app.infrastructure.adapters.session_recorder_sqla import SqlaSessionRecorder
from app.infrastructure.auth.adapters.data_mapper_sqla import (
    SqlaAuthSessionDataMapper,
)
from app.infrastructure.auth.adapters.identity_provider import (
    AuthSessionIdentityProvider,
)
from app.infrastructure.auth.adapters.transaction_manager_sqla import (
    SqlaAuthSessionTransactionManager,
)
from app.infrastructure.auth.handlers.log_in import LogInHandler
from app.infrastructure.auth.handlers.log_out import LogOutHandler
from app.infrastructure.auth.handlers.sign_up import SignUpHandler
from app.infrastructure.auth.handlers.refresh_token import RefreshTokenHandler
from app.infrastructure.auth.session.id_generator_str import (
    StrAuthSessionIdGenerator,
)
from app.infrastructure.auth.refresh_token.generator import RefreshTokenGenerator
from app.infrastructure.auth.session.ports.gateway import AuthSessionGateway
from app.infrastructure.auth.session.ports.transaction_manager import (
    AuthSessionTransactionManager,
)
from app.infrastructure.auth.session.ports.transport import AuthSessionTransport
from app.infrastructure.auth.session.service import AuthSessionService
from app.infrastructure.auth.session.timer_utc import UtcAuthSessionTimer
from app.application.common.ports.session_recorder import SessionRecorder
from app.application.common.ports.session_store import SessionStore
from app.application.common.ports.country_query_gateway import CountryQueryGateway
from app.application.common.ports.city_query_gateway import CityQueryGateway
from app.infrastructure.persistence_sqla.provider import (
    get_async_engine,
    get_async_session_factory,
    get_auth_async_session,
    get_main_async_session,
)
from app.presentation.http.auth.adapters.session_transport_jwt_header import (
    JwtHeaderAuthSessionTransport,
)
from app.infrastructure.adapters.session_store_sqla import SqlaSessionStore


class InfrastructureProvider(Provider):
    scope = Scope.REQUEST

    # Auth Services
    auth_session_service = provide(source=AuthSessionService)

    # Auth Ports Persistence
    auth_session_gateway = provide(
        source=SqlaAuthSessionDataMapper,
        provides=AuthSessionGateway,
    )
    # Session Recorder Port
    session_recorder = provide(
        source=SqlaSessionRecorder,
        provides=SessionRecorder,
    )
    auth_session_tx_manager = provide(
        source=SqlaAuthSessionTransactionManager,
        provides=AuthSessionTransactionManager,
    )

    # Auth Ports
    auth_session_transport = provide(
        source=JwtHeaderAuthSessionTransport,
        provides=AuthSessionTransport,
    )
    country_query_gateway = provide(
        source=SqlaCountryReader,
        provides=CountryQueryGateway,
    )
    city_query_gateway = provide(
        source=SqlaCityReader,
        provides=CityQueryGateway,
    )

    # Infrastructure Handlers
    infra_handlers = provide_all(
        SignUpHandler,
        LogInHandler,
        LogOutHandler,
        RefreshTokenHandler,
    )

    # Concrete Objects
    infra_objects = provide_all(
        StrAuthSessionIdGenerator,
        UtcAuthSessionTimer,
        RefreshTokenGenerator,
        AuthSessionIdentityProvider,
        SqlaAuthSessionDataMapper,
        SqlaAuthSessionTransactionManager,
        SqlaSessionRecorder,
        SqlaSessionStore,
        SqlaUserDataMapper,
        SqlaUserReader,
        SqlaMainTransactionManager,
    )


def infrastructure_provider() -> InfrastructureProvider:
    provider = InfrastructureProvider()

    # SQLA Persistence
    provider.provide(
        source=get_async_engine,
        scope=Scope.APP,
    )
    provider.provide(
        source=get_async_session_factory,
        scope=Scope.APP,
    )
    provider.provide(
        source=get_main_async_session,
        scope=Scope.REQUEST,
    )
    provider.provide(
        source=get_auth_async_session,
        scope=Scope.REQUEST,
    )
    return provider
