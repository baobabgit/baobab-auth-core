"""Tests de l'entité Permission."""

from datetime import UTC, datetime

from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestPermission:
    def test_BL_010_003_1_construction(self) -> None:
        perm = Permission(
            id=PermissionId("p1"),
            name=PermissionName("auth:user:read"),
            resource="user",
            action="read",
            is_system=False,
            created_at=_NOW,
        )
        assert perm.name == PermissionName("auth:user:read")
        assert perm.resource == "user"
        assert perm.action == "read"
        assert perm.is_system is False
        assert perm.description is None

    def test_BL_010_003_2_with_description(self) -> None:
        perm = Permission(
            id=PermissionId("p1"),
            name=PermissionName("auth:user:write"),
            resource="user",
            action="write",
            is_system=True,
            created_at=_NOW,
            description="Write permission",
        )
        assert perm.description == "Write permission"
