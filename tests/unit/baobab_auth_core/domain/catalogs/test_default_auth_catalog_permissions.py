"""Tests des permissions du DefaultAuthCatalog.

:spec: BL-040-002
"""

from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog
from baobab_auth_core.domain.value_objects.permission_name import PermissionName

_EXPECTED = (
    "auth:user:read",
    "auth:user:write",
    "auth:user:disable",
    "auth:role:read",
    "auth:role:write",
    "auth:session:read",
    "auth:session:revoke",
    "auth:audit:read",
    "auth:jwk:read",
    "auth:jwk:rotate",
)


class TestDefaultAuthCatalogPermissions:
    def test_BL_040_002_1_dix_permissions_exactes(self) -> None:
        perms = DefaultAuthCatalog().permissions()
        assert tuple(str(p.name) for p in perms) == _EXPECTED

    def test_BL_040_002_2_chaque_permission_systeme_complete(self) -> None:
        for perm in DefaultAuthCatalog().permissions():
            assert perm.is_system is True
            assert perm.resource
            assert perm.action
            assert perm.description
            assert perm.name == PermissionName(str(perm.name))

    def test_BL_040_002_3_ordre_deterministe(self) -> None:
        first = DefaultAuthCatalog().permissions()
        second = DefaultAuthCatalog().permissions()
        assert [str(p.name) for p in first] == [str(p.name) for p in second]
