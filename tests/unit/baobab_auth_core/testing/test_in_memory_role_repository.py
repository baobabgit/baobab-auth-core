"""Tests RBAC du fake InMemoryRoleRepository.

:spec: BL-030-003
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.testing.in_memory_role_repository import InMemoryRoleRepository

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestInMemoryRoleRepositoryRbac:
    def setup_method(self) -> None:
        self.repo = InMemoryRoleRepository()

    def _make_role(self, rid: str = "r1", name: str = "USER") -> Role:
        return Role(
            id=RoleId(rid),
            name=RoleName(name),
            is_system=False,
            created_at=_NOW,
            updated_at=_NOW,
        )

    def test_BL_030_003_1_list_roles_returns_tuple(self) -> None:
        self.repo.save(self._make_role("r1", "USER"))
        self.repo.save(self._make_role("r2", "ADMIN"))
        assert self.repo.list_roles() == (
            self._make_role("r1", "USER"),
            self._make_role("r2", "ADMIN"),
        )

    def test_BL_030_003_2_count_users_with_role_defaults_to_zero(self) -> None:
        assert self.repo.count_users_with_role(RoleName("USER")) == 0

    def test_BL_030_003_3_count_users_with_role_is_configurable(self) -> None:
        self.repo.set_users_with_role_count(RoleName("SUPER_ADMIN"), 2)
        assert self.repo.count_users_with_role(RoleName("SUPER_ADMIN")) == 2

    def test_BL_030_003_4_rejects_negative_role_user_count(self) -> None:
        with pytest.raises(ValueError, match="zéro"):
            self.repo.set_users_with_role_count(RoleName("USER"), -1)

    def test_BL_030_003_5_clear_resets_user_counts(self) -> None:
        self.repo.set_users_with_role_count(RoleName("USER"), 1)
        self.repo.clear()
        assert self.repo.count_users_with_role(RoleName("USER")) == 0
