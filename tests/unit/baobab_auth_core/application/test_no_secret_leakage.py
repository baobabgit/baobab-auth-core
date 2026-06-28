"""Test de sécurité — aucun secret ne fuit dans l'audit.

:spec: BL-020-008
"""

from baobab_auth_core.application.commands.authenticate_user_command import (
    AuthenticateUserCommand,
)
from baobab_auth_core.application.commands.refresh_session_command import (
    RefreshSessionCommand,
)
from baobab_auth_core.application.commands.register_user_command import (
    RegisterUserCommand,
)
from baobab_auth_core.application.use_cases.authenticate_user import AuthenticateUser
from baobab_auth_core.application.use_cases.refresh_session import RefreshSession
from baobab_auth_core.application.use_cases.register_user import RegisterUser

_SECRETS = ("Sup3rSecret!!", "hashed:", "fake-refresh:", "fake-token:")


class TestNoSecretLeakage:
    def test_BL_020_008_1_aucun_secret_dans_l_audit(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, hasher, tokens, ids, clock, uow
    ) -> None:
        register = RegisterUser(users, audit, hasher, ids, clock, uow)
        register.execute(
            RegisterUserCommand(email="bob@example.com", password="Sup3rSecret!!")
        )
        authenticate = AuthenticateUser(
            users, sessions, audit, hasher, tokens, ids, clock, uow
        )
        result = authenticate.execute(
            AuthenticateUserCommand(email="bob@example.com", password="Sup3rSecret!!")
        )
        refresh = RefreshSession(sessions, users, audit, tokens, ids, clock, uow)
        refresh.execute(
            RefreshSessionCommand(refresh_token=result.tokens.refresh_token)
        )

        haystack = "\n".join(
            f"{e.event_type}|{e.metadata}|{e.target_id}|{e.target_type}"
            for e in audit.all_events
        )
        assert audit.all_events
        for secret in _SECRETS:
            assert secret not in haystack
