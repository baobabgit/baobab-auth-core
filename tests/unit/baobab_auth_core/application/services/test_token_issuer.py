"""Tests du service TokenIssuer.

:spec: BL-020-002
"""

from datetime import UTC, datetime

from baobab_auth_core.application.services.token_issuer import TokenIssuer
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.policies.session_policy import SessionPolicy
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.testing.fake_token_provider import FakeTokenProvider

_NOW = datetime(2024, 1, 1, tzinfo=UTC)
_FUTURE = datetime(2099, 1, 1, tzinfo=UTC)


class TestTokenIssuer:
    def _session(self) -> Session:
        return Session(
            id=SessionId("s1"),
            user_id=UserId("u1"),
            refresh_token_id=TokenId("rtid-1"),
            status=SessionStatus.ACTIVE,
            created_at=_NOW,
            expires_at=_FUTURE,
        )

    def test_BL_020_002_1_emet_une_paire(self) -> None:
        issuer = TokenIssuer(FakeTokenProvider(), SessionPolicy())
        pair = issuer.issue(
            subject=AuthSubject("subj-1"),
            session=self._session(),
            roles=(RoleName("USER"),),
        )
        assert pair.token_type == "Bearer"
        assert pair.expires_in == SessionPolicy().access_token_ttl_seconds
        assert pair.refresh_expires_in == SessionPolicy().refresh_token_ttl_seconds
        assert pair.access_token
        assert pair.refresh_token

    def test_BL_020_002_2_refresh_token_porte_le_token_id(self) -> None:
        tokens = FakeTokenProvider()
        issuer = TokenIssuer(tokens)
        pair = issuer.issue(
            subject=AuthSubject("subj-1"),
            session=self._session(),
            roles=(),
        )
        payload = tokens.verify_refresh_token(pair.refresh_token)
        assert payload["refresh_token_id"] == "rtid-1"
