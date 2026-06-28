"""Tests du cas d'usage AuthenticateUser (auth + lockout).

:spec: BL-020-002, BL-020-003
"""

from datetime import UTC, datetime, timedelta

import pytest

from baobab_auth_core.application.commands.authenticate_user_command import (
    AuthenticateUserCommand,
)
from baobab_auth_core.application.use_cases.authenticate_user import AuthenticateUser
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.policies.session_policy import SessionPolicy
from baobab_auth_core.exceptions.auth import InvalidCredentialsError
from baobab_auth_core.exceptions.user import UserDisabledError, UserLockedError


class TestAuthenticateUser:
    def _uc(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, hasher, tokens, ids, clock, uow, policy=None
    ):
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

    def _types(self, audit):  # type: ignore[no-untyped-def]
        return [e.event_type for e in audit.all_events]

    def test_BL_020_002_1_login_nominal(  # type: ignore[no-untyped-def]
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
        uc = self._uc(users, sessions, audit, hasher, tokens, ids, clock, uow)
        result = uc.execute(
            AuthenticateUserCommand(email=valid_email, password=valid_password)
        )
        assert result.session.status == SessionStatus.ACTIVE
        assert result.tokens.access_token
        assert result.tokens.refresh_token
        assert sessions.get_by_id(result.session.id) is not None
        assert uow.committed is True
        assert AuditEventType.LOGIN_SUCCESS in self._types(audit)

    def test_BL_020_002_2_email_inconnu(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, hasher, tokens, ids, clock, uow, valid_password
    ) -> None:
        uc = self._uc(users, sessions, audit, hasher, tokens, ids, clock, uow)
        with pytest.raises(InvalidCredentialsError):
            uc.execute(
                AuthenticateUserCommand(
                    email="ghost@example.com", password=valid_password
                )
            )
        assert AuditEventType.LOGIN_FAILURE in self._types(audit)

    def test_BL_020_002_3_mauvais_mot_de_passe(  # type: ignore[no-untyped-def]
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
        uc = self._uc(users, sessions, audit, hasher, tokens, ids, clock, uow)
        with pytest.raises(InvalidCredentialsError):
            uc.execute(
                AuthenticateUserCommand(email=valid_email, password="WrongPass123!!")
            )
        assert AuditEventType.LOGIN_FAILURE in self._types(audit)

    def test_BL_020_003_1_verrouillage_apres_n_echecs(  # type: ignore[no-untyped-def]
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
        policy = SessionPolicy(max_failed_login_attempts=3)
        uc = self._uc(users, sessions, audit, hasher, tokens, ids, clock, uow, policy)
        for _ in range(3):
            with pytest.raises(InvalidCredentialsError):
                uc.execute(
                    AuthenticateUserCommand(email=valid_email, password="Nope12345!!")
                )
        from baobab_auth_core.domain.value_objects.email import Email

        locked = users.get_by_email(Email(valid_email))
        assert locked is not None
        assert locked.status == UserStatus.LOCKED
        assert AuditEventType.ACCOUNT_LOCKED in self._types(audit)

    def test_BL_020_003_2_compte_verrouille_refuse(  # type: ignore[no-untyped-def]
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
        user = make_active_user(status=UserStatus.LOCKED)
        user.locked_until = datetime(2099, 1, 1, tzinfo=UTC)
        users.save(user)
        uc = self._uc(users, sessions, audit, hasher, tokens, ids, clock, uow)
        with pytest.raises(UserLockedError):
            uc.execute(
                AuthenticateUserCommand(email=valid_email, password=valid_password)
            )

    def test_BL_020_003_3_auto_deverrouillage(  # type: ignore[no-untyped-def]
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
        user = make_active_user(status=UserStatus.LOCKED)
        user.locked_until = datetime(2024, 1, 1, tzinfo=UTC) - timedelta(seconds=1)
        users.save(user)
        uc = self._uc(users, sessions, audit, hasher, tokens, ids, clock, uow)
        result = uc.execute(
            AuthenticateUserCommand(email=valid_email, password=valid_password)
        )
        assert result.session.status == SessionStatus.ACTIVE
        assert AuditEventType.LOGIN_SUCCESS in self._types(audit)

    def test_BL_020_002_4_compte_desactive_refuse(  # type: ignore[no-untyped-def]
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
        users.save(make_active_user(status=UserStatus.DISABLED))
        uc = self._uc(users, sessions, audit, hasher, tokens, ids, clock, uow)
        with pytest.raises(UserDisabledError):
            uc.execute(
                AuthenticateUserCommand(email=valid_email, password=valid_password)
            )
