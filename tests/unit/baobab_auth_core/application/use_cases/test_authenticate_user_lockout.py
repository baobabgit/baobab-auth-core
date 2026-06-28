"""Tests ciblés du lockout d'AuthenticateUser (durcissement 0.4.0).

:spec: BL-040-014, BL-020-003
"""

import pytest

from baobab_auth_core.application.commands.authenticate_user_command import (
    AuthenticateUserCommand,
)
from baobab_auth_core.application.use_cases.authenticate_user import AuthenticateUser
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.policies.session_policy import SessionPolicy
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.exceptions.auth import InvalidCredentialsError


class TestAuthenticateUserLockout:
    def _uc(self, users, sessions, audit, hasher, tokens, ids, clock, uow, policy):  # type: ignore[no-untyped-def]
        return AuthenticateUser(
            users,
            sessions,
            audit,
            hasher,
            tokens,
            ids,
            clock,
            uow,
            session_policy=policy,
        )

    def test_BL_040_014_1_verrouillage_puis_audit(  # type: ignore[no-untyped-def]
        self,
        users,
        sessions,
        audit,
        hasher,
        tokens,
        ids,
        clock,
        uow,
        make_active_user,
        valid_email,
    ) -> None:
        users.save(make_active_user())
        policy = SessionPolicy(max_failed_login_attempts=2)
        uc = self._uc(users, sessions, audit, hasher, tokens, ids, clock, uow, policy)
        for _ in range(2):
            with pytest.raises(InvalidCredentialsError):
                uc.execute(
                    AuthenticateUserCommand(email=valid_email, password="Wr0ngPass!!")
                )
        locked = users.get_by_email(Email(valid_email))
        assert locked is not None
        assert locked.status == UserStatus.LOCKED
        types = [e.event_type for e in audit.all_events]
        assert AuditEventType.ACCOUNT_LOCKED in types
        assert AuditEventType.LOGIN_FAILURE in types

    def test_BL_040_014_2_succes_reinitialise_compteur(  # type: ignore[no-untyped-def]
        self,
        users,
        sessions,
        audit,
        hasher,
        tokens,
        ids,
        clock,
        uow,
        make_active_user,
        valid_email,
        valid_password,
    ) -> None:
        users.save(make_active_user())
        policy = SessionPolicy(max_failed_login_attempts=5)
        uc = self._uc(users, sessions, audit, hasher, tokens, ids, clock, uow, policy)
        with pytest.raises(InvalidCredentialsError):
            uc.execute(
                AuthenticateUserCommand(email=valid_email, password="Wr0ngPass!!")
            )
        uc.execute(AuthenticateUserCommand(email=valid_email, password=valid_password))
        user = users.get_by_email(Email(valid_email))
        assert user is not None
        assert user.failed_login_count == 0
