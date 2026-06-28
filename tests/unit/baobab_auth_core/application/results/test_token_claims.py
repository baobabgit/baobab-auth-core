"""Tests du DTO TokenClaims.

:spec: BL-020-007
"""

from datetime import UTC, datetime

from baobab_auth_core.application.results.token_claims import TokenClaims
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId

_NOW = datetime(2024, 1, 1, tzinfo=UTC)
_EXP = datetime(2024, 1, 1, 0, 15, tzinfo=UTC)


class TestTokenClaims:
    def test_BL_020_007_1_construction(self) -> None:
        claims = TokenClaims(
            subject=AuthSubject("subj-1"),
            session_id=SessionId("s1"),
            token_id=TokenId("t1"),
            roles=(RoleName("USER"),),
            permissions=(),
            issued_at=_NOW,
            expires_at=_EXP,
            issuer="baobab",
            audience="api",
        )
        assert claims.subject == AuthSubject("subj-1")
        assert claims.roles == (RoleName("USER"),)
        assert claims.permissions == ()
        assert claims.issuer == "baobab"
