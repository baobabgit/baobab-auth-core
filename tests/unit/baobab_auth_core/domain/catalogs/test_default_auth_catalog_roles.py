"""Tests des rôles du DefaultAuthCatalog.

:spec: BL-040-003
"""

from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog
from baobab_auth_core.domain.value_objects.role_name import RoleName

_EXPECTED = ("USER", "ADMIN", "SERVICE", "SUPER_ADMIN")


class TestDefaultAuthCatalogRoles:
    def test_BL_040_003_1_quatre_roles_systeme(self) -> None:
        roles = DefaultAuthCatalog().roles()
        assert tuple(str(r.name) for r in roles) == _EXPECTED

    def test_BL_040_003_2_roles_systeme(self) -> None:
        for role in DefaultAuthCatalog().roles():
            assert role.is_system is True
            assert role.name == RoleName(str(role.name))

    def test_BL_040_003_3_service_sans_permission(self) -> None:
        roles = {str(r.name): r for r in DefaultAuthCatalog().roles()}
        assert roles["SERVICE"].permission_names == ()

    def test_BL_040_003_4_super_admin_a_toutes_les_permissions(self) -> None:
        catalog = DefaultAuthCatalog()
        roles = {str(r.name): r for r in catalog.roles()}
        all_perms = tuple(p.name for p in catalog.permissions())
        assert roles["SUPER_ADMIN"].permission_names == all_perms
