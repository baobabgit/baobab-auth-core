"""Tests du cas d'usage RequestJwkRotation.

:spec: BL-040-008
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.commands.request_jwk_rotation_command import (
    RequestJwkRotationCommand,
)
from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.application.use_cases.request_jwk_rotation import (
    RequestJwkRotation,
)
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


class TestRequestJwkRotation:
    def setup_method(self) -> None:
        self.users = InMemoryUserRepository()
        self.roles = InMemoryRoleRepository()
        self.permissions = InMemoryPermissionRepository()
        self.audit = InMemoryAuditRepository()
        self.uow = InMemoryUnitOfWork()
        self.authorization = AuthorizationService(
            self.users, self.roles, self.permissions
        )
        self.use_case = RequestJwkRotation(
            self.authorization, self.audit, FakeIdGenerator(), FakeClock(_NOW), self.uow
        )
        for name in ("ADMIN", "SUPER_ADMIN"):
            self.roles.save(
                Role(
                    id=RoleId(f"role-{name.lower()}"),
                    name=RoleName(name),
                    is_system=True,
                    created_at=_NOW,
                    updated_at=_NOW,
                )
            )

    def _user(self, subject: str, role: str) -> None:
        self.users.save(
            User(
                id=UserId(subject),
                auth_subject=AuthSubject(subject),
                email=Email(f"{subject}@example.com"),
                password_hash=PasswordHash("hash-1"),
                status=UserStatus.ACTIVE,
                role_names=(RoleName(role),),
                created_at=_NOW,
                updated_at=_NOW,
            )
        )

    def test_BL_040_008_1_super_admin_declenche_rotation_critique(self) -> None:
        self._user("root", "SUPER_ADMIN")
        self.use_case.execute(RequestJwkRotationCommand(actor_subject="root"))
        assert self.uow.committed
        assert len(self.audit.all_events) == 1
        event = self.audit.all_events[0]
        assert event.event_type == AuditEventType.JWK_ROTATION_REQUESTED
        assert event.severity == AuditSeverity.CRITICAL

    def test_BL_040_008_2_admin_refuse(self) -> None:
        self._user("admin", "ADMIN")
        with pytest.raises(ForbiddenError):
            self.use_case.execute(RequestJwkRotationCommand(actor_subject="admin"))
        assert self.audit.all_events == []
