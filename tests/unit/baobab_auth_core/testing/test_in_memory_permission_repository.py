"""Tests RBAC du fake InMemoryPermissionRepository.

:spec: BL-030-003
"""

from datetime import UTC, datetime

from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.testing.in_memory_permission_repository import (
    InMemoryPermissionRepository,
)

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestInMemoryPermissionRepositoryRbac:
    def setup_method(self) -> None:
        self.repo = InMemoryPermissionRepository()

    def _make_permission(
        self,
        pid: str = "p1",
        name: str = "auth:user:read",
    ) -> Permission:
        return Permission(
            id=PermissionId(pid),
            name=PermissionName(name),
            resource="user",
            action="read",
            is_system=False,
            created_at=_NOW,
        )

    def test_BL_030_003_1_list_permissions_returns_tuple(self) -> None:
        self.repo.save(self._make_permission("p1", "auth:user:read"))
        self.repo.save(self._make_permission("p2", "auth:user:write"))
        assert self.repo.list_permissions() == (
            self._make_permission("p1", "auth:user:read"),
            self._make_permission("p2", "auth:user:write"),
        )

    def test_BL_030_003_2_list_all_remains_retrocompatible(self) -> None:
        self.repo.save(self._make_permission())
        assert self.repo.list_all() == [self._make_permission()]
