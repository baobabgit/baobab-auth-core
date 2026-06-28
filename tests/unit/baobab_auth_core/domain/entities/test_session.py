"""Tests de l'entité Session."""

from datetime import UTC, datetime

from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId

_NOW = datetime(2024, 1, 1, tzinfo=UTC)
_EXPIRES = datetime(2024, 2, 1, tzinfo=UTC)


class TestSession:
    def test_BL_010_003_1_construction_minimal(self) -> None:
        s = Session(
            id=SessionId("s1"),
            user_id=UserId("u1"),
            refresh_token_id=TokenId("t1"),
            status=SessionStatus.ACTIVE,
            created_at=_NOW,
            expires_at=_EXPIRES,
        )
        assert s.status == SessionStatus.ACTIVE
        assert s.revoked_at is None
        assert s.last_used_at is None
        assert s.user_agent is None
        assert s.ip_address is None
        assert s.device_label is None

    def test_BL_010_003_2_construction_full(self) -> None:
        s = Session(
            id=SessionId("s1"),
            user_id=UserId("u1"),
            refresh_token_id=TokenId("t1"),
            status=SessionStatus.ACTIVE,
            created_at=_NOW,
            expires_at=_EXPIRES,
            user_agent="Mozilla/5.0",
            ip_address="127.0.0.1",
            device_label="My Phone",
        )
        assert s.user_agent == "Mozilla/5.0"
        assert s.ip_address == "127.0.0.1"
        assert s.device_label == "My Phone"

    def _make(self, status: SessionStatus = SessionStatus.ACTIVE) -> Session:
        return Session(
            id=SessionId("s1"),
            user_id=UserId("u1"),
            refresh_token_id=TokenId("t1"),
            status=status,
            created_at=_NOW,
            expires_at=_EXPIRES,
        )

    def test_BL_020_004_1_is_active_et_is_expired(self) -> None:
        s = self._make()
        assert s.is_active(_NOW) is True
        assert s.is_expired(_NOW) is False
        assert s.is_expired(_EXPIRES) is True
        assert s.is_active(_EXPIRES) is False

    def test_BL_020_004_2_mark_used(self) -> None:
        s = self._make()
        s.mark_used(_NOW)
        assert s.last_used_at == _NOW

    def test_BL_020_004_3_rotate_refresh_token(self) -> None:
        s = self._make()
        s.rotate_refresh_token(TokenId("t2"), _NOW)
        assert s.refresh_token_id == TokenId("t2")
        assert s.last_used_at == _NOW

    def test_BL_020_006_1_revoke_idempotent(self) -> None:
        s = self._make()
        s.revoke(_NOW)
        assert s.status == SessionStatus.REVOKED
        assert s.revoked_at == _NOW
        s.revoke(_EXPIRES)  # idempotent : ne change pas la date de révocation
        assert s.revoked_at == _NOW
        assert s.is_active(_NOW) is False

    def test_BL_020_004_4_expire(self) -> None:
        s = self._make()
        s.expire(_NOW)
        assert s.status == SessionStatus.EXPIRED
        assert s.is_expired(_NOW) is True
