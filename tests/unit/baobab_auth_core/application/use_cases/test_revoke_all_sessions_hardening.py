"""Tests de durcissement du cas d'usage RevokeAllSessions.

:spec: BL-040-014
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.commands.revoke_all_sessions_command import (
    RevokeAllSessionsCommand,
)
from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.application.use_cases.revoke_all_sessions import RevokeAllSessions
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.authorization import ForbiddenError
from baobab_auth_core.testing.fake_clock import FakeClock
from baobab_auth_core.testing.fake_id_generator import FakeIdGenerator
from baobab_auth_core.testing.in_memory_audit_repository import InMemoryAuditRepository
from baobab_auth_core.testing.in_memory_permission_repository import (
    InMemoryPermissionRepository,
)
from baobab_auth_core.testing.in_memory_role_repository import InMemoryRoleRepository
from baobab_auth_core.testing.in_memory_session_repository import (
    InMemorySessionRepository,
)
from baobab_auth_core.testing.in_memory_unit_of_work import InMemoryUnitOfWork
from baobab_auth_core.testing.in_memory_user_repository import InMemoryUserRepository

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestRevokeAllSessionsHardening:
    def setup_method(self) -> None:
        self.users = InMemoryUserRepository()
        self.roles = InMemoryRoleRepository()
        self.permissions = InMemoryPermissionRepository()
        self.sessions = InMemorySessionRepository()
        self.audit = InMemoryAuditRepository()
        self.uow = InMemoryUnitOfWork()
        self.authorization = AuthorizationService(
            self.users, self.roles, self.permissions
        )
        self.use_case = RevokeAllSessions(
            self.authorization,
            self.users,
            self.sessions,
            self.audit,
            FakeIdGenerator(),
            FakeClock(_NOW),
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

    def _user(self, uid: str, role: str) -> None:
        self.users.save(
            User(
                id=UserId(uid),
                auth_subject=AuthSubject(f"subj-{uid}"),
                email=Email(f"{uid}@example.com"),
                password_hash=PasswordHash("hash-1"),
                status=UserStatus.ACTIVE,
                role_names=(RoleName(role),),
                created_at=_NOW,
                updated_at=_NOW,
            )
        )

    def _sessions_for(self, uid: str, count: int) -> None:
        for i in range(count):
            self.sessions.save(
                Session(
                    id=SessionId(f"sess-{uid}-{i}"),
                    user_id=UserId(uid),
                    refresh_token_id=TokenId(f"rt-{uid}-{i}"),
                    status=SessionStatus.ACTIVE,
                    created_at=_NOW,
                    expires_at=datetime(2099, 1, 1, tzinfo=UTC),
                )
            )

    def test_BL_040_014_1_utilisateur_revoque_ses_sessions(self) -> None:
        self._user("alice", "USER")
        self._sessions_for("alice", 2)
        count = self.use_case.execute(
            RevokeAllSessionsCommand(actor_subject="subj-alice", target_user_id="alice")
        )
        assert count == 2
        event = self.audit.all_events[0]
        assert event.event_type == AuditEventType.ALL_SESSIONS_REVOKED
        assert event.metadata == {"count": 2}

    def test_BL_040_014_2_admin_revoque_compte_standard(self) -> None:
        self._user("admin", "ADMIN")
        self._user("bob", "USER")
        self._sessions_for("bob", 1)
        count = self.use_case.execute(
            RevokeAllSessionsCommand(actor_subject="subj-admin", target_user_id="bob")
        )
        assert count == 1

    def test_BL_040_014_3_acteur_non_autorise_refuse(self) -> None:
        self._user("eve", "USER")
        self._user("bob", "USER")
        self._sessions_for("bob", 1)
        with pytest.raises(ForbiddenError):
            self.use_case.execute(
                RevokeAllSessionsCommand(actor_subject="subj-eve", target_user_id="bob")
            )

    def test_BL_040_014_4_admin_ne_neutralise_pas_super_admin(self) -> None:
        self._user("admin", "ADMIN")
        self._user("root", "SUPER_ADMIN")
        self._sessions_for("root", 1)
        with pytest.raises(ForbiddenError):
            self.use_case.execute(
                RevokeAllSessionsCommand(
                    actor_subject="subj-admin", target_user_id="root"
                )
            )

    def test_BL_040_014_5_super_admin_revoque_super_admin(self) -> None:
        self._user("root", "SUPER_ADMIN")
        self._user("root2", "SUPER_ADMIN")
        self._sessions_for("root2", 1)
        count = self.use_case.execute(
            RevokeAllSessionsCommand(actor_subject="subj-root", target_user_id="root2")
        )
        assert count == 1
