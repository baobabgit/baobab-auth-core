"""Tests de RolePolicy."""

import dataclasses

from baobab_auth_core.domain.policies.role_policy import RolePolicy
from baobab_auth_core.domain.value_objects.role_name import RoleName


class TestRolePolicy:
    def test_BL_010_004_1_defaults(self) -> None:
        p = RolePolicy()
        assert p.default_role_name == RoleName("USER")
        assert p.super_admin_role_name == RoleName("SUPER_ADMIN")
        assert p.enforce_last_super_admin is True

    def test_BL_010_004_2_custom(self) -> None:
        p = RolePolicy(
            default_role_name=RoleName("MEMBER"),
            super_admin_role_name=RoleName("ROOT"),
            enforce_last_super_admin=False,
        )
        assert p.default_role_name == RoleName("MEMBER")
        assert p.enforce_last_super_admin is False

    def test_BL_010_004_3_frozen(self) -> None:
        import pytest

        p = RolePolicy()
        with pytest.raises(dataclasses.FrozenInstanceError):
            p.enforce_last_super_admin = False  # type: ignore[misc]

    def test_BL_030_003_1_allows_non_super_admin_removal(self) -> None:
        p = RolePolicy()
        assert p.can_remove_role(RoleName("ADMIN"), users_with_role=1) is True

    def test_BL_030_003_2_blocks_last_super_admin_removal(self) -> None:
        p = RolePolicy()
        assert p.can_remove_role(RoleName("SUPER_ADMIN"), users_with_role=1) is False

    def test_BL_030_003_3_allows_super_admin_removal_when_others_remain(self) -> None:
        p = RolePolicy()
        assert p.can_remove_role(RoleName("SUPER_ADMIN"), users_with_role=2) is True

    def test_BL_030_003_4_can_disable_last_super_admin_protection(self) -> None:
        p = RolePolicy(enforce_last_super_admin=False)
        assert p.can_remove_role(RoleName("SUPER_ADMIN"), users_with_role=1) is True
