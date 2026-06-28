"""Tests du DTO SessionDTO.

:spec: BL-020-007
"""

from datetime import UTC, datetime

from baobab_auth_core.application.results.session_dto import SessionDTO
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId

_NOW = datetime(2024, 1, 1, tzinfo=UTC)
_FUTURE = datetime(2099, 1, 1, tzinfo=UTC)


class TestSessionDTO:
    def test_BL_020_007_1_from_session_sans_refresh_token(self) -> None:
        session = Session(
            id=SessionId("s1"),
            user_id=UserId("u1"),
            refresh_token_id=TokenId("secret-rtid"),
            status=SessionStatus.ACTIVE,
            created_at=_NOW,
            expires_at=_FUTURE,
            ip_address="127.0.0.1",
            device_label="Phone",
        )
        dto = SessionDTO.from_session(session)
        assert dto.id == SessionId("s1")
        assert dto.status == SessionStatus.ACTIVE
        assert dto.ip_address == "127.0.0.1"
        assert dto.device_label == "Phone"
        assert not hasattr(dto, "refresh_token_id")
        assert "secret-rtid" not in repr(dto)
