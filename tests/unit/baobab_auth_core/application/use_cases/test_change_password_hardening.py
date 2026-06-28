"""Tests de durcissement du cas d'usage ChangePassword.

:spec: BL-040-013
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.commands.change_password_command import (
    ChangePasswordCommand,
)
from baobab_auth_core.application.use_cases.change_password import ChangePassword
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.auth import InvalidCredentialsError
from baobab_auth_core.exceptions.validation import ValidationError, WeakPasswordError

_NEW = "An0therStr0ng!!"


def _active_session(user_id: str) -> Session:
    return Session(
        id=SessionId(f"sess-{user_id}"),
        user_id=UserId(user_id),
        refresh_token_id=TokenId(f"rt-{user_id}"),
        status=SessionStatus.ACTIVE,
        created_at=datetime(2024, 1, 1, tzinfo=UTC),
        expires_at=datetime(2099, 1, 1, tzinfo=UTC),
    )


class TestChangePasswordHardening:
    def _uc(self, users, sessions, audit, hasher, ids, clock, uow):  # type: ignore[no-untyped-def]
        return ChangePassword(users, sessions, audit, hasher, ids, clock, uow)

    def test_BL_040_013_1_change_nominal_et_revoque_sessions(  # type: ignore[no-untyped-def]
        self,
        users,
        sessions,
        audit,
        hasher,
        ids,
        clock,
        uow,
        make_active_user,
        valid_password,
    ) -> None:
        user = make_active_user()
        users.save(user)
        sessions.save(_active_session(str(user.id)))
        uc = self._uc(users, sessions, audit, hasher, ids, clock, uow)
        revoked = uc.execute(
            ChangePasswordCommand(
                auth_subject=str(user.auth_subject),
                old_password=valid_password,
                new_password=_NEW,
            )
        )
        assert revoked == 1
        stored = users.get_by_auth_subject(user.auth_subject)
        assert stored is not None
        assert hasher.verify(PlainPassword(_NEW), stored.password_hash)
        assert sessions.get_by_id(SessionId(f"sess-{user.id}")).status == (
            SessionStatus.REVOKED
        )
        assert any(
            e.event_type == AuditEventType.PASSWORD_CHANGED for e in audit.all_events
        )
        text = "\n".join(str(e.metadata) for e in audit.all_events)
        assert valid_password not in text
        assert _NEW not in text

    def test_BL_040_013_2_ancien_mot_de_passe_incorrect(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, hasher, ids, clock, uow, make_active_user
    ) -> None:
        users.save(make_active_user())
        uc = self._uc(users, sessions, audit, hasher, ids, clock, uow)
        with pytest.raises(InvalidCredentialsError):
            uc.execute(
                ChangePasswordCommand(
                    auth_subject="subj-alice",
                    old_password="WrongOldPass1!",
                    new_password=_NEW,
                )
            )

    def test_BL_040_013_3_nouveau_trop_faible(  # type: ignore[no-untyped-def]
        self,
        users,
        sessions,
        audit,
        hasher,
        ids,
        clock,
        uow,
        make_active_user,
        valid_password,
    ) -> None:
        users.save(make_active_user())
        uc = self._uc(users, sessions, audit, hasher, ids, clock, uow)
        with pytest.raises(WeakPasswordError):
            uc.execute(
                ChangePasswordCommand(
                    auth_subject="subj-alice",
                    old_password=valid_password,
                    new_password="short",
                )
            )

    def test_BL_040_013_4_nouveau_identique_a_ancien(  # type: ignore[no-untyped-def]
        self,
        users,
        sessions,
        audit,
        hasher,
        ids,
        clock,
        uow,
        make_active_user,
        valid_password,
    ) -> None:
        users.save(make_active_user())
        uc = self._uc(users, sessions, audit, hasher, ids, clock, uow)
        with pytest.raises(ValidationError):
            uc.execute(
                ChangePasswordCommand(
                    auth_subject="subj-alice",
                    old_password=valid_password,
                    new_password=valid_password,
                )
            )
