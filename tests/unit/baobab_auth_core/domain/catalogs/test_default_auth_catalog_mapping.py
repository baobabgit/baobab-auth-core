"""Tests du mapping rôle → permissions du DefaultAuthCatalog.

:spec: BL-040-004
"""

from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_name import RoleName


def _names(perms: tuple[PermissionName, ...]) -> set[str]:
    return {str(p) for p in perms}


class TestDefaultAuthCatalogMapping:
    def test_BL_040_004_1_user_lecture_seule(self) -> None:
        mapping = DefaultAuthCatalog().role_permissions()
        assert _names(mapping[RoleName("USER")]) == {
            "auth:user:read",
            "auth:session:read",
        }

    def test_BL_040_004_2_admin_large_sans_jwk_rotate(self) -> None:
        mapping = DefaultAuthCatalog().role_permissions()
        admin = _names(mapping[RoleName("ADMIN")])
        assert "auth:jwk:rotate" not in admin
        assert "auth:role:write" not in admin
        assert {"auth:user:write", "auth:session:revoke", "auth:audit:read"} <= admin

    def test_BL_040_004_3_service_vide(self) -> None:
        mapping = DefaultAuthCatalog().role_permissions()
        assert mapping[RoleName("SERVICE")] == ()

    def test_BL_040_004_4_super_admin_toutes(self) -> None:
        catalog = DefaultAuthCatalog()
        mapping = catalog.role_permissions()
        assert _names(mapping[RoleName("SUPER_ADMIN")]) == {
            str(p.name) for p in catalog.permissions()
        }
