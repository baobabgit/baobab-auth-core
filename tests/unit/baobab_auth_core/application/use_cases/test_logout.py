"""Tests du cas d'usage Logout.

:spec: BL-020-005
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.commands.logout_command import LogoutCommand
from baobab_auth_core.application.use_cases.logout import Logout
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.exceptions.authorization import ForbiddenError

_NOW = datetime(2024, 1, 1, tzinfo=UTC)
_FUTURE = datetime(2099, 1, 1, tzinfo=UTC)


def _seed_session(users, sessions, make_active_user):  # type: ignore[no-untyped-def]
    user = make_active_user()
    users.save(user)
    session = Session(
        id=SessionId("sess-1"),
        user_id=user.id,
        refresh_token_id=TokenId("rtid-1"),
        status=SessionStatus.ACTIVE,
        created_at=_NOW,
        expires_at=_FUTURE,
    )
    sessions.save(session)
    return user, session


class TestLogout:
    def _uc(self, sessions, users, audit, ids, clock, uow):  # type: ignore[no-untyped-def]
        return Logout(sessions, users, audit, ids, clock, uow)

    def test_BL_020_005_1_logout_nominal(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, ids, clock, uow, make_active_user
    ) -> None:
        user, session = _seed_session(users, sessions, make_active_user)
        uc = self._uc(sessions, users, audit, ids, clock, uow)
        uc.execute(
            LogoutCommand(session_id=session.id, actor_subject=user.auth_subject)
        )
        assert sessions.get_by_id(session.id).status == SessionStatus.REVOKED
        assert any(e.event_type == AuditEventType.LOGOUT for e in audit.all_events)

    def test_BL_020_005_2_logout_idempotent(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, ids, clock, uow, make_active_user
    ) -> None:
        user, session = _seed_session(users, sessions, make_active_user)
        uc = self._uc(sessions, users, audit, ids, clock, uow)
        cmd = LogoutCommand(session_id=session.id, actor_subject=user.auth_subject)
        uc.execute(cmd)
        uc.execute(cmd)  # idempotent : pas d'erreur, pas de second LOGOUT
        logout_events = [
            e for e in audit.all_events if e.event_type == AuditEventType.LOGOUT
        ]
        assert len(logout_events) == 1

    def test_BL_020_005_3_session_absente_no_op(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, ids, clock, uow
    ) -> None:
        uc = self._uc(sessions, users, audit, ids, clock, uow)
        uc.execute(
            LogoutCommand(
                session_id=SessionId("nope"), actor_subject=AuthSubject("subj-x")
            )
        )
        assert audit.all_events == []

    def test_BL_020_005_4_session_d_autrui_interdite(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, ids, clock, uow, make_active_user
    ) -> None:
        _, session = _seed_session(users, sessions, make_active_user)
        uc = self._uc(sessions, users, audit, ids, clock, uow)
        with pytest.raises(ForbiddenError):
            uc.execute(
                LogoutCommand(
                    session_id=session.id, actor_subject=AuthSubject("intruder")
                )
            )
