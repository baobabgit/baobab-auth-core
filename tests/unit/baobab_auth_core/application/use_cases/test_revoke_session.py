"""Tests du cas d'usage RevokeSession.

:spec: BL-020-006
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.commands.revoke_session_command import (
    RevokeSessionCommand,
)
from baobab_auth_core.application.use_cases.revoke_session import RevokeSession
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.session import SessionNotFoundError

_NOW = datetime(2024, 1, 1, tzinfo=UTC)
_FUTURE = datetime(2099, 1, 1, tzinfo=UTC)


def _seed(sessions, status=SessionStatus.ACTIVE):  # type: ignore[no-untyped-def]
    session = Session(
        id=SessionId("sess-1"),
        user_id=UserId("user-1"),
        refresh_token_id=TokenId("rtid-1"),
        status=status,
        created_at=_NOW,
        expires_at=_FUTURE,
        revoked_at=_NOW if status == SessionStatus.REVOKED else None,
    )
    sessions.save(session)
    return session


class TestRevokeSession:
    def _uc(self, sessions, audit, ids, clock, uow):  # type: ignore[no-untyped-def]
        return RevokeSession(sessions, audit, ids, clock, uow)

    def test_BL_020_006_1_revocation_nominale(  # type: ignore[no-untyped-def]
        self, sessions, audit, ids, clock, uow
    ) -> None:
        session = _seed(sessions)
        uc = self._uc(sessions, audit, ids, clock, uow)
        uc.execute(
            RevokeSessionCommand(
                actor_subject=AuthSubject("admin"), session_id=session.id
            )
        )
        assert sessions.get_by_id(session.id).status == SessionStatus.REVOKED
        assert any(
            e.event_type == AuditEventType.SESSION_REVOKED for e in audit.all_events
        )

    def test_BL_020_006_2_revocation_idempotente(  # type: ignore[no-untyped-def]
        self, sessions, audit, ids, clock, uow
    ) -> None:
        session = _seed(sessions, status=SessionStatus.REVOKED)
        uc = self._uc(sessions, audit, ids, clock, uow)
        uc.execute(RevokeSessionCommand(actor_subject=None, session_id=session.id))
        assert audit.all_events == []  # no-op idempotent

    def test_BL_020_006_3_session_inconnue_refusee(  # type: ignore[no-untyped-def]
        self, sessions, audit, ids, clock, uow
    ) -> None:
        uc = self._uc(sessions, audit, ids, clock, uow)
        with pytest.raises(SessionNotFoundError):
            uc.execute(
                RevokeSessionCommand(actor_subject=None, session_id=SessionId("ghost"))
            )
