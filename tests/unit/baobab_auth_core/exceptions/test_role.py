"""Tests des exceptions liées aux rôles et permissions."""

import pytest

from baobab_auth_core.exceptions import (
    LastAdminRoleRemovalError as ExportedLastAdminRoleRemovalError,
)
from baobab_auth_core.exceptions import (
    RoleError as ExportedRoleError,
)
from baobab_auth_core.exceptions.base import BaobabAuthCoreError
from baobab_auth_core.exceptions.role import (
    LastAdminRoleRemovalError,
    LastSuperAdminRoleRemovalError,
    PermissionNotFoundError,
    RoleError,
    RoleNotFoundError,
)


class TestRoleExceptions:
    def test_BL_010_005_1_all_inherit_base(self) -> None:
        for cls in (
            RoleError,
            RoleNotFoundError,
            PermissionNotFoundError,
            LastSuperAdminRoleRemovalError,
        ):
            assert issubclass(cls, BaobabAuthCoreError)
            assert issubclass(cls, RoleError)

    def test_BL_010_005_2_role_not_found(self) -> None:
        with pytest.raises(RoleNotFoundError):
            raise RoleNotFoundError("role missing")

    def test_BL_010_005_3_permission_not_found(self) -> None:
        with pytest.raises(PermissionNotFoundError):
            raise PermissionNotFoundError("perm missing")

    def test_BL_010_005_4_last_super_admin(self) -> None:
        with pytest.raises(LastSuperAdminRoleRemovalError):
            raise LastSuperAdminRoleRemovalError("cannot remove")

    def test_BL_030_006_1_last_admin_alias_retrocompatible(self) -> None:
        assert LastAdminRoleRemovalError is LastSuperAdminRoleRemovalError
        with pytest.raises(LastAdminRoleRemovalError):
            raise LastSuperAdminRoleRemovalError("cannot remove")

    def test_BL_030_006_2_exports_publics_rbac(self) -> None:
        assert ExportedRoleError is RoleError
        assert ExportedLastAdminRoleRemovalError is LastSuperAdminRoleRemovalError
