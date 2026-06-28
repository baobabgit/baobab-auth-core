"""Tests des règles SUPER_ADMIN de RolePolicy.

:spec: BL-040-005, BL-040-006
"""

from baobab_auth_core.domain.policies.role_policy import RolePolicy
from baobab_auth_core.domain.value_objects.role_name import RoleName

_ADMIN = (RoleName("ADMIN"),)
_SUPER = (RoleName("SUPER_ADMIN"),)
_SA = RoleName("SUPER_ADMIN")
_USER = RoleName("USER")


class TestRolePolicySuperAdmin:
    def test_BL_040_005_1_is_super_admin_role(self) -> None:
        p = RolePolicy()
        assert p.is_super_admin_role(_SA) is True
        assert p.is_super_admin_role(_USER) is False

    def test_BL_040_005_2_admin_ne_peut_assigner_super_admin(self) -> None:
        p = RolePolicy()
        assert p.can_assign_role(_ADMIN, _SA) is False
        assert p.can_assign_role(_SUPER, _SA) is True

    def test_BL_040_005_3_assigner_role_standard_autorise(self) -> None:
        p = RolePolicy()
        assert p.can_assign_role(_ADMIN, _USER) is True

    def test_BL_040_006_1_admin_ne_peut_retirer_super_admin(self) -> None:
        p = RolePolicy()
        assert p.can_remove_role(_ADMIN, _SA) is False
        assert p.can_remove_role(_SUPER, _SA) is True

    def test_BL_040_006_2_retirer_role_standard_autorise(self) -> None:
        p = RolePolicy()
        assert p.can_remove_role(_ADMIN, _USER) is True
