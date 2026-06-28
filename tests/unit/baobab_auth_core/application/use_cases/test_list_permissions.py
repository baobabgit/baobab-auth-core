"""Tests du cas d'usage ListPermissions.

:spec: BL-050-007
"""

from datetime import UTC, datetime

from baobab_auth_core.application.use_cases.list_permissions import ListPermissions
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestListPermissions:
    def test_BL_050_007_1_liste_les_permissions(  # type: ignore[no-untyped-def]
        self, permissions
    ) -> None:
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
        result = ListPermissions(permissions).execute()
        assert PermissionName("auth:user:read") in {p.name for p in result}

    def test_BL_050_007_2_liste_vide(  # type: ignore[no-untyped-def]
        self, permissions
    ) -> None:
        assert ListPermissions(permissions).execute() == ()
