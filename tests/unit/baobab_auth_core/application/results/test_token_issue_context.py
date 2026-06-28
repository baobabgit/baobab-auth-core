"""Tests du DTO TokenIssueContext.

:spec: BL-050-002
"""

from datetime import UTC, datetime

from baobab_auth_core.application.results.token_issue_context import TokenIssueContext
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.user_id import UserId

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestTokenIssueContext:
    def test_BL_050_002_1_construction(self) -> None:
        ctx = TokenIssueContext(
            subject=AuthSubject("subj-1"),
            user_id=UserId("u1"),
            session_id=SessionId("s1"),
            roles=(RoleName("USER"),),
            permissions=(PermissionName("auth:user:read"),),
            issued_at=_NOW,
            access_expires_at=_NOW,
            refresh_expires_at=_NOW,
            issuer="baobab",
            audience="api",
        )
        assert ctx.subject == AuthSubject("subj-1")
        assert ctx.session_id == SessionId("s1")
        assert ctx.permissions == (PermissionName("auth:user:read"),)
        assert ctx.issuer == "baobab"
