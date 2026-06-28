"""Tests du cas d'usage GetCurrentUser.

:spec: BL-050-007
"""

from datetime import UTC, datetime

from baobab_auth_core.application.queries.get_current_user_query import (
    GetCurrentUserQuery,
)
from baobab_auth_core.application.use_cases.get_current_user import GetCurrentUser
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestGetCurrentUser:
    def test_BL_050_007_1_agrege_roles_et_permissions(  # type: ignore[no-untyped-def]
        self, users, roles, permissions, authorization, make_active_user, make_role
    ) -> None:
        users.save(make_active_user())
        roles.save(make_role("USER", ("auth:user:read",)))
        permissions.save(
            Permission(
                id=PermissionId("p1"),
                name=PermissionName("auth:user:read"),
                resource="user",
                action="read",
                is_system=True,
                created_at=_NOW,
            )
        )
        result = GetCurrentUser(users, authorization).execute(
            GetCurrentUserQuery(auth_subject="subj-alice")
        )
        assert PermissionName("auth:user:read") in result.permissions
        assert result.roles == result.role_names
        assert not hasattr(result, "password_hash")
