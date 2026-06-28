"""Tests du cas d'usage RefreshSession.

:spec: BL-020-004
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.commands.refresh_session_command import (
    RefreshSessionCommand,
)
from baobab_auth_core.application.use_cases.refresh_session import RefreshSession
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.exceptions.auth import TokenInvalidError
from baobab_auth_core.exceptions.session import (
    SessionExpiredError,
    SessionNotFoundError,
    SessionRevokedError,
)

_NOW = datetime(2024, 1, 1, tzinfo=UTC)
_FUTURE = datetime(2099, 1, 1, tzinfo=UTC)
_PAST = datetime(2020, 1, 1, tzinfo=UTC)


def _seed(  # type: ignore[no-untyped-def]
    users,
    sessions,
    tokens,
    make_active_user,
    *,
    expires=_FUTURE,
    status=SessionStatus.ACTIVE,
):
    user = make_active_user()
    users.save(user)
    rtid = tokens.generate_token_id()
    session = Session(
        id=SessionId("sess-1"),
        user_id=user.id,
        refresh_token_id=rtid,
        status=status,
        created_at=_NOW,
        expires_at=expires,
    )
    if status == SessionStatus.REVOKED:
        session.revoked_at = _NOW
    sessions.save(session)
    refresh_token = tokens.create_refresh_token(str(user.auth_subject), rtid, 3600)
    return user, session, refresh_token


class TestRefreshSession:
    def _uc(self, sessions, users, audit, tokens, ids, clock, uow):  # type: ignore[no-untyped-def]
        return RefreshSession(sessions, users, audit, tokens, ids, clock, uow)

    def test_BL_020_004_1_refresh_nominal(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, tokens, ids, clock, uow, make_active_user
    ) -> None:
        _, session, refresh_token = _seed(users, sessions, tokens, make_active_user)
        old_rtid = session.refresh_token_id
        uc = self._uc(sessions, users, audit, tokens, ids, clock, uow)
        result = uc.execute(RefreshSessionCommand(refresh_token=refresh_token))
        assert result.tokens.access_token
        assert result.tokens.refresh_token
        assert session.refresh_token_id != old_rtid  # rotation
        assert uow.committed is True
        assert any(
            e.event_type == AuditEventType.SESSION_REFRESHED for e in audit.all_events
        )
        assert refresh_token not in str(audit.all_events)

    def test_BL_020_004_2_refresh_session_expiree(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, tokens, ids, clock, uow, make_active_user
    ) -> None:
        _, _, refresh_token = _seed(
            users, sessions, tokens, make_active_user, expires=_PAST
        )
        uc = self._uc(sessions, users, audit, tokens, ids, clock, uow)
        with pytest.raises(SessionExpiredError):
            uc.execute(RefreshSessionCommand(refresh_token=refresh_token))

    def test_BL_020_004_3_refresh_session_revoquee(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, tokens, ids, clock, uow, make_active_user
    ) -> None:
        _, _, refresh_token = _seed(
            users, sessions, tokens, make_active_user, status=SessionStatus.REVOKED
        )
        uc = self._uc(sessions, users, audit, tokens, ids, clock, uow)
        with pytest.raises(SessionRevokedError):
            uc.execute(RefreshSessionCommand(refresh_token=refresh_token))

    def test_BL_020_004_4_token_invalide(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, tokens, ids, clock, uow
    ) -> None:
        uc = self._uc(sessions, users, audit, tokens, ids, clock, uow)
        with pytest.raises(TokenInvalidError):
            uc.execute(RefreshSessionCommand(refresh_token="garbage-token"))

    def test_BL_020_004_5_session_introuvable(  # type: ignore[no-untyped-def]
        self, users, sessions, audit, tokens, ids, clock, uow
    ) -> None:
        orphan = tokens.create_refresh_token("subj-x", TokenId("orphan-rtid"), 3600)
        uc = self._uc(sessions, users, audit, tokens, ids, clock, uow)
        with pytest.raises(SessionNotFoundError):
            uc.execute(RefreshSessionCommand(refresh_token=orphan))
