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
