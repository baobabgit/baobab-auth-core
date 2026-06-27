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
