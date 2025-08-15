from dishka import Provider, Scope, provide, provide_all

from app.application.commands.user.activate_user import ActivateUserInteractor
from app.application.commands.user.change_password import ChangePasswordInteractor
from app.application.commands.user.deactivate_user import DeactivateUserInteractor
from app.application.commands.user.grant_admin import GrantAdminInteractor
from app.application.commands.user.revoke_admin import RevokeAdminInteractor
from app.application.common.ports.access_revoker import AccessRevoker
from app.application.common.ports.flusher import Flusher
from app.application.common.ports.identity_provider import IdentityProvider
from app.application.common.ports.transaction_manager import (
    TransactionManager,
)
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.application.common.ports.user_query_gateway import UserQueryGateway
from app.application.common.services.current_user import CurrentUserService
from app.application.queries.list_users import ListUsersQueryService
from app.application.atlas.queries import (
    SearchCountriesQueryService,
    SearchCitiesQueryService,
    ListStatesByCountryQueryService,
)
from app.infrastructure.adapters.main_flusher_sqla import SqlaMainFlusher
from app.infrastructure.adapters.main_transaction_manager_sqla import (
    SqlaMainTransactionManager,
)
from app.infrastructure.adapters.user_data_mapper_sqla import (
    SqlaUserDataMapper,
)
from app.infrastructure.adapters.user_reader_sqla import SqlaUserReader
from app.infrastructure.auth.adapters.access_revoker import (
    AuthSessionAccessRevoker,
)
from app.infrastructure.auth.adapters.identity_provider import (
    AuthSessionIdentityProvider,
)
from app.domain.services.user import UserService
from app.domain.ports.password_hasher import PasswordHasher
from app.domain.ports.user_id_generator import UserIdGenerator
from app.infrastructure.adapters.password_hasher_bcrypt import BcryptPasswordHasher, PasswordPepper
from app.infrastructure.adapters.user_id_generator_uuid import UuidUserIdGenerator
from app.setup.config.security import PasswordSettings


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    # Services
    services = provide_all(
        CurrentUserService,
        UserService,
    )

    # Domain service dependencies
    user_id_generator = provide(source=UuidUserIdGenerator, provides=UserIdGenerator)
    password_hasher = provide(source=BcryptPasswordHasher, provides=PasswordHasher)

    @staticmethod
    def _password_pepper(settings: PasswordSettings) -> PasswordPepper:  # factory
        return PasswordPepper(settings.pepper)

    pepper = provide(source=_password_pepper)

    # Ports Auth
    access_revoker = provide(
        source=AuthSessionAccessRevoker,
        provides=AccessRevoker,
    )
    identity_provider = provide(
        source=AuthSessionIdentityProvider,
        provides=IdentityProvider,
    )

    # Ports Persistence
    tx_manager = provide(
        source=SqlaMainTransactionManager,
        provides=TransactionManager,
    )
    flusher = provide(
        source=SqlaMainFlusher,
        provides=Flusher,
    )
    user_command_gateway = provide(
        source=SqlaUserDataMapper,
        provides=UserCommandGateway,
    )
    user_query_gateway = provide(
        source=SqlaUserReader,
        provides=UserQueryGateway,
    )

    # Commands
    commands = provide_all(
        ActivateUserInteractor,
        ChangePasswordInteractor,
        DeactivateUserInteractor,
        GrantAdminInteractor,
        RevokeAdminInteractor,
    )

    # Queries
    query_services = provide_all(
        ListUsersQueryService,
        SearchCountriesQueryService,
        SearchCitiesQueryService,
        ListStatesByCountryQueryService,
    )
