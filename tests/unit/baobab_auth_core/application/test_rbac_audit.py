"""Tests de couverture RBAC et d'audit sans fuite de secret.

:spec: BL-030-007
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.commands.assign_role_command import (
    AssignRoleCommand,
)
from baobab_auth_core.application.commands.remove_role_command import (
    RemoveRoleCommand,
)
from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.application.use_cases.assign_role import AssignRole
from baobab_auth_core.application.use_cases.remove_role import RemoveRole
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.authorization import (
    ForbiddenError,
    PermissionDeniedError,
)
from baobab_auth_core.exceptions.role import LastSuperAdminRoleRemovalError
from baobab_auth_core.testing.fake_clock import FakeClock
from baobab_auth_core.testing.fake_id_generator import FakeIdGenerator
from baobab_auth_core.testing.in_memory_audit_repository import (
    InMemoryAuditRepository,
)
from baobab_auth_core.testing.in_memory_permission_repository import (
    InMemoryPermissionRepository,
)
from baobab_auth_core.testing.in_memory_role_repository import InMemoryRoleRepository
from baobab_auth_core.testing.in_memory_unit_of_work import InMemoryUnitOfWork
from baobab_auth_core.testing.in_memory_user_repository import InMemoryUserRepository

_NOW = datetime(2024, 1, 1, tzinfo=UTC)
_SECRET_HASH = "TOP_SECRET_HASH_VALUE"
_FORBIDDEN_MARKERS = (
    _SECRET_HASH,
    "password",
    "token",
    "secret",
    "hashed:",
    "fake-refresh:",
    "fake-token:",
)


class TestRbacAuditCoverage:
    def setup_method(self) -> None:
        self.users = InMemoryUserRepository()
        self.roles = InMemoryRoleRepository()
        self.permissions = InMemoryPermissionRepository()
        self.audit = InMemoryAuditRepository()
        self.ids = FakeIdGenerator()
        self.clock = FakeClock(_NOW)
        self.uow = InMemoryUnitOfWork()
        self.authorization = AuthorizationService(
            self.users,
            self.roles,
            self.permissions,
        )
        self.assign_role = AssignRole(
            self.users,
            self.roles,
            self.authorization,
            self.audit,
            self.ids,
            self.clock,
            self.uow,
        )
        self.remove_role = RemoveRole(
            self.users,
            self.roles,
            self.authorization,
            self.audit,
            self.ids,
            self.clock,
            self.uow,
        )

    def _make_permission(self, name: str) -> Permission:
        permission_name = PermissionName(name)
        return Permission(
            id=PermissionId(f"permission-{permission_name.value.replace(':', '-')}"),
            name=permission_name,
            resource=permission_name.value.split(":")[1],
            action=permission_name.value.split(":")[2],
            is_system=False,
            created_at=_NOW,
        )

    def _make_role(
        self,
        name: str,
        permission_names: tuple[PermissionName, ...] = (),
    ) -> Role:
        return Role(
            id=RoleId(f"role-{name.lower()}"),
            name=RoleName(name),
            is_system=False,
            created_at=_NOW,
            updated_at=_NOW,
            permission_names=permission_names,
        )

    def _make_user(
        self,
        user_id: str,
        subject: str,
        roles: tuple[RoleName, ...],
        password_hash: str = _SECRET_HASH,
    ) -> User:
        return User(
            id=UserId(user_id),
            auth_subject=AuthSubject(subject),
            email=Email(f"{user_id}@example.com"),
            password_hash=PasswordHash(password_hash),
            status=UserStatus.ACTIVE,
            role_names=roles,
            created_at=_NOW,
            updated_at=_NOW,
        )

    def _seed_rbac_catalog(self) -> None:
        user_read = PermissionName("auth:user:read")
        role_write = PermissionName("auth:role:write")
        self.permissions.save(self._make_permission("auth:user:read"))
        self.permissions.save(self._make_permission("auth:role:write"))
        self.roles.save(self._make_role("ADMIN", (user_read, role_write)))
        self.roles.save(self._make_role("SUPER_ADMIN"))
        self.roles.save(self._make_role("SUPPORT", (role_write,)))
        self.roles.save(self._make_role("USER", (user_read,)))
        self.roles.save(self._make_role("AUDITOR", (role_write,)))

    def _audit_haystack(self) -> str:
        return "\n".join(
            (
                f"{event.event_type}|{event.metadata}|{event.target_id}|"
                f"{event.target_type}|{event.actor_subject}"
            )
            for event in self.audit.all_events
        ).lower()

    def test_BL_030_007_1_agrege_et_deduplique_permissions_multi_roles(self) -> None:
        # Arrange
        self._seed_rbac_catalog()
        self.users.save(
            self._make_user(
                "user-1",
                "subject-1",
                (RoleName("USER"), RoleName("ADMIN"), RoleName("AUDITOR")),
            )
        )

        # Act
        context = self.authorization.build_context("subject-1")

        # Assert
        assert context.permissions == (
            PermissionName("auth:user:read"),
            PermissionName("auth:role:write"),
        )

    def test_BL_030_007_2_refuse_role_et_permission(self) -> None:
        # Arrange
        self._seed_rbac_catalog()
        self.users.save(self._make_user("user-1", "subject-1", (RoleName("USER"),)))
        context = self.authorization.build_context("subject-1")

        # Act / Assert
        with pytest.raises(ForbiddenError, match="ADMIN"):
            self.authorization.require_role(context, "ADMIN")
        with pytest.raises(PermissionDeniedError, match="auth:role:write"):
            self.authorization.require_permission(context, "auth:role:write")

    def test_BL_030_007_3_assignation_et_retrait_nominaux_et_idempotents(self) -> None:
        # Arrange
        self._seed_rbac_catalog()
        self.users.save(
            self._make_user("actor-1", "subject-admin", (RoleName("ADMIN"),))
        )
        self.users.save(
            self._make_user("target-1", "subject-target", (RoleName("USER"),))
        )

        # Act — assignation nominale
        self.assign_role.execute(
            AssignRoleCommand(
                actor_subject="subject-admin",
                target_user_id="target-1",
                role_name="support",
            )
        )
        target_after_assign = self.users.get_by_id(UserId("target-1"))
        assert target_after_assign is not None
        assert target_after_assign.role_names == (
            RoleName("USER"),
            RoleName("SUPPORT"),
        )
        assert len(self.audit.all_events) == 1
        assert self.audit.all_events[0].event_type == AuditEventType.ROLE_ASSIGNED

        # Act — assignation idempotente
        self.assign_role.execute(
            AssignRoleCommand(
                actor_subject="subject-admin",
                target_user_id="target-1",
                role_name="support",
            )
        )
        assert len(self.audit.all_events) == 1

        # Act — retrait nominal
        self.remove_role.execute(
            RemoveRoleCommand(
                actor_subject="subject-admin",
                target_user_id="target-1",
                role_name="support",
            )
        )
        target_after_remove = self.users.get_by_id(UserId("target-1"))
        assert target_after_remove is not None
        assert target_after_remove.role_names == (RoleName("USER"),)
        assert len(self.audit.all_events) == 2
        assert self.audit.all_events[1].event_type == AuditEventType.ROLE_REMOVED

        # Act — retrait idempotent
        self.remove_role.execute(
            RemoveRoleCommand(
                actor_subject="subject-admin",
                target_user_id="target-1",
                role_name="support",
            )
        )
        assert len(self.audit.all_events) == 2

    def test_BL_030_007_4_protege_le_dernier_super_admin(self) -> None:
        # Arrange
        self._seed_rbac_catalog()
        self.roles.set_users_with_role_count(RoleName("SUPER_ADMIN"), 1)
        self.users.save(
            self._make_user("actor-1", "subject-root", (RoleName("SUPER_ADMIN"),))
        )
        self.users.save(
            self._make_user("target-1", "subject-target", (RoleName("SUPER_ADMIN"),))
        )

        # Act / Assert
        with pytest.raises(LastSuperAdminRoleRemovalError):
            self.remove_role.execute(
                RemoveRoleCommand(
                    actor_subject="subject-root",
                    target_user_id="target-1",
                    role_name="SUPER_ADMIN",
                )
            )
        assert self.audit.all_events == []

    def test_BL_030_007_5_audits_rbac_sans_secret(self) -> None:
        # Arrange
        self._seed_rbac_catalog()
        self.users.save(
            self._make_user("actor-1", "subject-admin", (RoleName("ADMIN"),))
        )
        self.users.save(
            self._make_user(
                "target-1",
                "subject-target",
                (RoleName("USER"),),
                password_hash=_SECRET_HASH,
            )
        )

        # Act
        self.assign_role.execute(
            AssignRoleCommand(
                actor_subject="subject-admin",
                target_user_id="target-1",
                role_name="support",
            )
        )
        self.remove_role.execute(
            RemoveRoleCommand(
                actor_subject="subject-admin",
                target_user_id="target-1",
                role_name="support",
            )
        )

        # Assert
        assert len(self.audit.all_events) == 2
        event_types = {event.event_type for event in self.audit.all_events}
        assert event_types == {
            AuditEventType.ROLE_ASSIGNED,
            AuditEventType.ROLE_REMOVED,
        }
        haystack = self._audit_haystack()
        for marker in _FORBIDDEN_MARKERS:
            assert marker.lower() not in haystack
