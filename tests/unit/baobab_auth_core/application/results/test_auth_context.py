"""Tests du DTO AuthContext.

:spec: BL-030-001
"""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.results.auth_context import AuthContext
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.user_id import UserId

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestAuthContext:
    def test_BL_030_001_1_deduplicates_roles_and_permissions(self) -> None:
        # Arrange
        role = RoleName("ADMIN")
        permission = PermissionName("auth:user:read")

        # Act
        context = AuthContext(
            auth_subject=AuthSubject("subject-1"),
            user_id=UserId("user-1"),
            session_id=SessionId("session-1"),
            roles=(role, RoleName("admin"), RoleName("USER")),
            permissions=(permission, PermissionName("auth:user:read")),
            authenticated_at=_NOW,
        )

        # Assert
        assert context.roles == (RoleName("ADMIN"), RoleName("USER"))
        assert context.permissions == (PermissionName("auth:user:read"),)

    def test_BL_030_001_2_checks_roles_from_value_objects_or_strings(self) -> None:
        # Arrange
        context = AuthContext(
            auth_subject=AuthSubject("subject-1"),
            user_id="user-1",
            session_id=None,
            roles=(RoleName("ADMIN"),),
            permissions=(),
            authenticated_at=_NOW,
        )

        # Act / Assert
        assert context.has_role(RoleName("ADMIN"))
        assert context.has_role("admin")
        assert context.has_any_role(["USER", RoleName("ADMIN")])
        assert not context.has_role("USER")
        assert not context.has_any_role(["USER", "SUPPORT"])

    def test_BL_030_001_3_checks_permissions(self) -> None:
        # Arrange
        context = AuthContext(
            auth_subject=AuthSubject("subject-1"),
            user_id=UserId("user-1"),
            session_id=None,
            roles=(),
            permissions=(
                PermissionName("auth:user:read"),
                PermissionName("auth:role:write"),
            ),
            authenticated_at=_NOW,
        )

        # Act / Assert
        assert context.has_permission(PermissionName("auth:user:read"))
        assert context.has_permission("auth:role:write")
        assert context.has_any_permission(["auth:user:delete", "auth:user:read"])
        assert context.has_all_permissions(["auth:user:read", "auth:role:write"])
        assert not context.has_permission("auth:user:delete")
        assert not context.has_all_permissions(["auth:user:read", "auth:user:delete"])

    def test_BL_030_001_4_is_immutable_and_secret_free(self) -> None:
        # Arrange
        context = AuthContext(
            auth_subject=AuthSubject("subject-1"),
            user_id=UserId("user-1"),
            session_id=None,
            roles=(RoleName("USER"),),
            permissions=(PermissionName("auth:user:read"),),
            authenticated_at=None,
        )

        # Act / Assert
        with pytest.raises(FrozenInstanceError):
            context.roles = ()  # type: ignore[misc]
        assert not hasattr(context, "password")
        assert not hasattr(context, "password_hash")
        assert "secret" not in repr(context).lower()
