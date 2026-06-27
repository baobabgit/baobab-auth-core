"""Tests des exceptions liées aux rôles et permissions."""

import pytest

from baobab_auth_core.exceptions.base import BaobabAuthCoreError
from baobab_auth_core.exceptions.role import (
    LastSuperAdminRoleRemovalError,
    PermissionNotFoundError,
    RoleNotFoundError,
)


class TestRoleExceptions:
    def test_BL_010_005_1_all_inherit_base(self) -> None:
        for cls in (
            RoleNotFoundError,
            PermissionNotFoundError,
            LastSuperAdminRoleRemovalError,
        ):
            assert issubclass(cls, BaobabAuthCoreError)

    def test_BL_010_005_2_role_not_found(self) -> None:
        with pytest.raises(RoleNotFoundError):
            raise RoleNotFoundError("role missing")

    def test_BL_010_005_3_permission_not_found(self) -> None:
        with pytest.raises(PermissionNotFoundError):
            raise PermissionNotFoundError("perm missing")

    def test_BL_010_005_4_last_super_admin(self) -> None:
        with pytest.raises(LastSuperAdminRoleRemovalError):
            raise LastSuperAdminRoleRemovalError("cannot remove")
