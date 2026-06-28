"""Tests des règles strictes SUPER_ADMIN dans AssignRole et RemoveRole.

:spec: BL-040-005, BL-040-006
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.commands.assign_role_command import AssignRoleCommand
from baobab_auth_core.application.commands.remove_role_command import RemoveRoleCommand
from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.application.use_cases.assign_role import AssignRole
from baobab_auth_core.application.use_cases.remove_role import RemoveRole
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.authorization import ForbiddenError
from baobab_auth_core.exceptions.role import LastSuperAdminRoleRemovalError
from baobab_auth_core.testing.fake_clock import FakeClock
from baobab_auth_core.testing.fake_id_generator import FakeIdGenerator
from baobab_auth_core.testing.in_memory_audit_repository import InMemoryAuditRepository
from baobab_auth_core.testing.in_memory_permission_repository import (
    InMemoryPermissionRepository,
)
from baobab_auth_core.testing.in_memory_role_repository import InMemoryRoleRepository
from baobab_auth_core.testing.in_memory_unit_of_work import InMemoryUnitOfWork
from baobab_auth_core.testing.in_memory_user_repository import InMemoryUserRepository

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestSuperAdminGuards:
    def setup_method(self) -> None:
        self.users = InMemoryUserRepository()
        self.roles = InMemoryRoleRepository()
        self.permissions = InMemoryPermissionRepository()
        self.audit = InMemoryAuditRepository()
        self.ids = FakeIdGenerator()
        self.clock = FakeClock(_NOW)
        self.uow = InMemoryUnitOfWork()
        self.authorization = AuthorizationService(
            self.users, self.roles, self.permissions
        )
        self.assign = AssignRole(
            self.users,
            self.roles,
            self.authorization,
            self.audit,
            self.ids,
            self.clock,
            self.uow,
        )
        self.remove = RemoveRole(
            self.users,
            self.roles,
            self.authorization,
            self.audit,
            self.ids,
            self.clock,
            self.uow,
        )
        for name in ("USER", "ADMIN", "SUPER_ADMIN"):
            self.roles.save(
                Role(
                    id=RoleId(f"role-{name.lower()}"),
                    name=RoleName(name),
                    is_system=True,
                    created_at=_NOW,
                    updated_at=_NOW,
                )
            )

    def _user(self, uid: str, subject: str, roles: tuple[RoleName, ...]) -> User:
        user = User(
            id=UserId(uid),
            auth_subject=AuthSubject(subject),
            email=Email(f"{uid}@example.com"),
            password_hash=PasswordHash("hash-1"),
            status=UserStatus.ACTIVE,
            role_names=roles,
            created_at=_NOW,
            updated_at=_NOW,
        )
        self.users.save(user)
        return user

    def test_BL_040_005_1_admin_ne_peut_attribuer_super_admin(self) -> None:
        self._user("actor", "subj-admin", (RoleName("ADMIN"),))
        self._user("target", "subj-target", ())
        with pytest.raises(ForbiddenError):
            self.assign.execute(
                AssignRoleCommand(
                    actor_subject="subj-admin",
                    target_user_id="target",
                    role_name="SUPER_ADMIN",
                )
            )
        assert self.audit.all_events == []

    def test_BL_040_005_2_super_admin_peut_attribuer_super_admin(self) -> None:
        self._user("actor", "subj-root", (RoleName("SUPER_ADMIN"),))
        self._user("target", "subj-target", ())
        self.assign.execute(
            AssignRoleCommand(
                actor_subject="subj-root",
                target_user_id="target",
                role_name="SUPER_ADMIN",
            )
        )
        target = self.users.get_by_id(UserId("target"))
        assert target is not None
        assert target.has_role(RoleName("SUPER_ADMIN"))

    def test_BL_040_006_1_admin_ne_peut_retirer_super_admin(self) -> None:
        self._user("actor", "subj-admin", (RoleName("ADMIN"),))
        self._user("target", "subj-target", (RoleName("SUPER_ADMIN"),))
        self.roles.set_users_with_role_count(RoleName("SUPER_ADMIN"), 3)
        with pytest.raises(ForbiddenError):
            self.remove.execute(
                RemoveRoleCommand(
                    actor_subject="subj-admin",
                    target_user_id="target",
                    role_name="SUPER_ADMIN",
                )
            )

    def test_BL_040_006_2_super_admin_retire_super_admin_si_autres_restent(
        self,
    ) -> None:
        self._user("actor", "subj-root", (RoleName("SUPER_ADMIN"),))
        self._user("target", "subj-target", (RoleName("SUPER_ADMIN"),))
        self.roles.set_users_with_role_count(RoleName("SUPER_ADMIN"), 2)
        self.remove.execute(
            RemoveRoleCommand(
                actor_subject="subj-root",
                target_user_id="target",
                role_name="SUPER_ADMIN",
            )
        )
        target = self.users.get_by_id(UserId("target"))
        assert target is not None
        assert not target.has_role(RoleName("SUPER_ADMIN"))

    def test_BL_040_006_3_dernier_super_admin_protege(self) -> None:
        self._user("actor", "subj-root", (RoleName("SUPER_ADMIN"),))
        self._user("target", "subj-target", (RoleName("SUPER_ADMIN"),))
        self.roles.set_users_with_role_count(RoleName("SUPER_ADMIN"), 1)
        with pytest.raises(LastSuperAdminRoleRemovalError):
            self.remove.execute(
                RemoveRoleCommand(
                    actor_subject="subj-root",
                    target_user_id="target",
                    role_name="SUPER_ADMIN",
                )
            )
