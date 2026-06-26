"""Tests de l'entité Role."""

from datetime import UTC, datetime

from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestRole:
    def test_BL_010_003_1_construction(self) -> None:
        role = Role(
            id=RoleId("r1"),
            name=RoleName("USER"),
            is_system=False,
            created_at=_NOW,
            updated_at=_NOW,
        )
        assert role.name == RoleName("USER")
        assert role.is_system is False
        assert role.description is None
        assert role.permission_names == ()

    def test_BL_010_003_2_with_permissions(self) -> None:
        role = Role(
            id=RoleId("r1"),
            name=RoleName("ADMIN"),
            is_system=True,
            created_at=_NOW,
            updated_at=_NOW,
            description="Administrator role",
            permission_names=(PermissionName("auth:user:read"),),
        )
        assert len(role.permission_names) == 1
        assert role.is_system is True
        assert role.description == "Administrator role"
