"""Tests du cas d'usage RemoveRole.

:spec: BL-030-005
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.commands.remove_role_command import (
    RemoveRoleCommand,
)
from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.application.use_cases.remove_role import RemoveRole
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.authorization import ForbiddenError
from baobab_auth_core.exceptions.role import (
    LastSuperAdminRoleRemovalError,
    RoleNotFoundError,
)
from baobab_auth_core.exceptions.user import UserNotFoundError
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


class TestRemoveRole:
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
        self.use_case = RemoveRole(
            self.users,
            self.roles,
            self.authorization,
            self.audit,
            self.ids,
            self.clock,
            self.uow,
        )

    def _make_user(
        self,
        user_id: str,
        subject: str,
        roles: tuple[RoleName, ...],
    ) -> User:
        return User(
            id=UserId(user_id),
            auth_subject=AuthSubject(subject),
            email=Email(f"{user_id}@example.com"),
            password_hash=PasswordHash("hash-1"),
            status=UserStatus.ACTIVE,
            role_names=roles,
            created_at=_NOW,
            updated_at=_NOW,
        )

    def _make_role(self, name: str) -> Role:
        return Role(
            id=RoleId(f"role-{name.lower()}"),
            name=RoleName(name),
            is_system=False,
            created_at=_NOW,
            updated_at=_NOW,
        )

    def _seed_roles(self) -> None:
        self.roles.save(self._make_role("ADMIN"))
        self.roles.save(self._make_role("SUPER_ADMIN"))
        self.roles.save(self._make_role("SUPPORT"))
        self.roles.save(self._make_role("USER"))

    def test_BL_030_005_1_retire_un_role_et_audite(self) -> None:
        # Arrange
        self._seed_roles()
        self.users.save(
            self._make_user("actor-1", "subject-admin", (RoleName("ADMIN"),))
        )
        self.users.save(
            self._make_user(
                "target-1",
                "subject-target",
                (RoleName("USER"), RoleName("SUPPORT")),
            )
        )
        command = RemoveRoleCommand(
            actor_subject="subject-admin",
            target_user_id="target-1",
            role_name="support",
            ip_address="192.0.2.20",
            user_agent="pytest",
        )

        # Act
        self.use_case.execute(command)

        # Assert
        target = self.users.get_by_id(UserId("target-1"))
        assert target is not None
        assert target.role_names == (RoleName("USER"),)
        assert self.uow.committed
        assert not self.uow.rolled_back
        assert len(self.audit.all_events) == 1
        event = self.audit.all_events[0]
        assert event.event_type == AuditEventType.ROLE_REMOVED
        assert event.severity == AuditSeverity.WARNING
        assert event.actor_subject == AuthSubject("subject-admin")
        assert event.target_type == "user"
        assert event.target_id == "target-1"
        assert event.ip_address == "192.0.2.20"
        assert event.user_agent == "pytest"
        assert event.metadata == {"role": "SUPPORT", "target_user_id": "target-1"}
        assert "hash" not in repr(event.metadata).lower()

    def test_BL_030_005_2_super_admin_est_autorise(self) -> None:
        # Arrange
        self._seed_roles()
        self.users.save(
            self._make_user("actor-1", "subject-root", (RoleName("SUPER_ADMIN"),))
        )
        self.users.save(
            self._make_user("target-1", "subject-target", (RoleName("USER"),))
        )

        # Act
        self.use_case.execute(
            RemoveRoleCommand(
                actor_subject=AuthSubject("subject-root"),
                target_user_id=UserId("target-1"),
                role_name=RoleName("USER"),
            )
        )

        # Assert
        target = self.users.get_by_id(UserId("target-1"))
        assert target is not None
        assert target.role_names == ()

    def test_BL_030_005_3_retrait_idempotent(self) -> None:
        # Arrange
        self._seed_roles()
        self.users.save(
            self._make_user("actor-1", "subject-admin", (RoleName("ADMIN"),))
        )
        self.users.save(self._make_user("target-1", "subject-target", ()))

        # Act
        self.use_case.execute(
            RemoveRoleCommand(
                actor_subject="subject-admin",
                target_user_id="target-1",
                role_name="SUPPORT",
            )
        )

        # Assert
        target = self.users.get_by_id(UserId("target-1"))
        assert target is not None
        assert target.role_names == ()
        assert self.audit.all_events == []
        assert not self.uow.committed

    def test_BL_030_005_4_protege_le_dernier_super_admin(self) -> None:
        # Arrange
        self._seed_roles()
        self.roles.set_users_with_role_count(RoleName("SUPER_ADMIN"), 1)
        self.users.save(
            self._make_user("actor-1", "subject-root", (RoleName("SUPER_ADMIN"),))
        )
        self.users.save(
            self._make_user(
                "target-1",
                "subject-target",
                (RoleName("SUPER_ADMIN"),),
            )
        )

        # Act / Assert
        with pytest.raises(LastSuperAdminRoleRemovalError):
            self.use_case.execute(
                RemoveRoleCommand(
                    actor_subject="subject-root",
                    target_user_id="target-1",
                    role_name="SUPER_ADMIN",
                )
            )
        target = self.users.get_by_id(UserId("target-1"))
        assert target is not None
        assert target.role_names == (RoleName("SUPER_ADMIN"),)
        assert self.audit.all_events == []

    def test_BL_030_005_5_autorise_si_plusieurs_super_admins(self) -> None:
        # Arrange
        self._seed_roles()
        self.roles.set_users_with_role_count(RoleName("SUPER_ADMIN"), 2)
        self.users.save(
            self._make_user("actor-1", "subject-root", (RoleName("SUPER_ADMIN"),))
        )
        self.users.save(
            self._make_user(
                "target-1",
                "subject-target",
                (RoleName("SUPER_ADMIN"),),
            )
        )

        # Act
        self.use_case.execute(
            RemoveRoleCommand(
                actor_subject="subject-root",
                target_user_id="target-1",
                role_name="SUPER_ADMIN",
            )
        )

        # Assert
        target = self.users.get_by_id(UserId("target-1"))
        assert target is not None
        assert target.role_names == ()

    def test_BL_030_005_6_acteur_non_autorise_refuse(self) -> None:
        # Arrange
        self._seed_roles()
        self.users.save(self._make_user("actor-1", "subject-user", (RoleName("USER"),)))
        self.users.save(
            self._make_user("target-1", "subject-target", (RoleName("SUPPORT"),))
        )

        # Act / Assert
        with pytest.raises(ForbiddenError):
            self.use_case.execute(
                RemoveRoleCommand(
                    actor_subject="subject-user",
                    target_user_id="target-1",
                    role_name="SUPPORT",
                )
            )
        assert self.audit.all_events == []

    def test_BL_030_005_7_cible_inconnue_refusee(self) -> None:
        # Arrange
        self._seed_roles()
        self.users.save(
            self._make_user("actor-1", "subject-admin", (RoleName("ADMIN"),))
        )

        # Act / Assert
        with pytest.raises(UserNotFoundError, match="missing"):
            self.use_case.execute(
                RemoveRoleCommand(
                    actor_subject="subject-admin",
                    target_user_id="missing",
                    role_name="SUPPORT",
                )
            )

    def test_BL_030_005_8_role_inconnu_refuse(self) -> None:
        # Arrange
        self._seed_roles()
        self.users.save(
            self._make_user("actor-1", "subject-admin", (RoleName("ADMIN"),))
        )
        self.users.save(self._make_user("target-1", "subject-target", ()))

        # Act / Assert
        with pytest.raises(RoleNotFoundError, match="UNKNOWN"):
            self.use_case.execute(
                RemoveRoleCommand(
                    actor_subject="subject-admin",
                    target_user_id="target-1",
                    role_name="UNKNOWN",
                )
            )
