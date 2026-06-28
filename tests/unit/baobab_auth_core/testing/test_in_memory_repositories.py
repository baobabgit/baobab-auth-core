"""Tests des repositories in-memory."""

from datetime import UTC, datetime

from baobab_auth_core.domain.entities.audit_event import AuditEvent
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.audit_event_id import AuditEventId
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.testing.in_memory_audit_repository import InMemoryAuditRepository
from baobab_auth_core.testing.in_memory_permission_repository import (
    InMemoryPermissionRepository,
)
from baobab_auth_core.testing.in_memory_role_repository import InMemoryRoleRepository
from baobab_auth_core.testing.in_memory_session_repository import (
    InMemorySessionRepository,
)
from baobab_auth_core.testing.in_memory_user_repository import InMemoryUserRepository

_NOW = datetime(2024, 1, 1, tzinfo=UTC)
_EXPIRES = datetime(2024, 2, 1, tzinfo=UTC)


def _make_user(uid: str = "u1", email: str = "alice@example.com") -> User:
    return User(
        id=UserId(uid),
        auth_subject=AuthSubject(f"subj-{uid}"),
        email=Email(email),
        password_hash=PasswordHash("hashed"),
        status=UserStatus.ACTIVE,
        role_names=(RoleName("USER"),),
        created_at=_NOW,
        updated_at=_NOW,
    )


class TestInMemoryUserRepository:
    def setup_method(self) -> None:
        self.repo = InMemoryUserRepository()

    def test_BL_010_007_1_save_and_get_by_id(self) -> None:
        user = _make_user()
        self.repo.save(user)
        result = self.repo.get_by_id(UserId("u1"))
        assert result is not None
        assert result.id == UserId("u1")

    def test_BL_010_007_2_get_by_id_not_found(self) -> None:
        assert self.repo.get_by_id(UserId("unknown")) is None

    def test_BL_010_007_3_get_by_email(self) -> None:
        user = _make_user()
        self.repo.save(user)
        result = self.repo.get_by_email(Email("alice@example.com"))
        assert result is not None

    def test_BL_010_007_4_get_by_email_not_found(self) -> None:
        assert self.repo.get_by_email(Email("x@x.com")) is None

    def test_BL_010_007_5_get_by_auth_subject(self) -> None:
        user = _make_user()
        self.repo.save(user)
        result = self.repo.get_by_auth_subject(AuthSubject("subj-u1"))
        assert result is not None

    def test_BL_010_007_6_get_by_auth_subject_not_found(self) -> None:
        assert self.repo.get_by_auth_subject(AuthSubject("unknown")) is None

    def test_BL_010_007_7_delete(self) -> None:
        user = _make_user()
        self.repo.save(user)
        self.repo.delete(UserId("u1"))
        assert self.repo.get_by_id(UserId("u1")) is None

    def test_BL_010_007_8_delete_nonexistent_no_error(self) -> None:
        self.repo.delete(UserId("nope"))

    def test_BL_010_007_9_exists_by_email(self) -> None:
        user = _make_user()
        self.repo.save(user)
        assert self.repo.exists_by_email(Email("alice@example.com")) is True
        assert self.repo.exists_by_email(Email("bob@example.com")) is False

    def test_BL_010_007_10_clear(self) -> None:
        self.repo.save(_make_user())
        self.repo.clear()
        assert self.repo.get_by_id(UserId("u1")) is None


class TestInMemoryRoleRepository:
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

    def test_BL_010_007_11_save_and_get_by_id(self) -> None:
        role = self._make_role()
        self.repo.save(role)
        assert self.repo.get_by_id(RoleId("r1")) is not None

    def test_BL_010_007_12_get_by_name(self) -> None:
        role = self._make_role()
        self.repo.save(role)
        assert self.repo.get_by_name(RoleName("USER")) is not None

    def test_BL_010_007_13_get_by_name_not_found(self) -> None:
        assert self.repo.get_by_name(RoleName("ADMIN")) is None

    def test_BL_010_007_14_list_all(self) -> None:
        self.repo.save(self._make_role("r1", "USER"))
        self.repo.save(self._make_role("r2", "ADMIN"))
        assert len(self.repo.list_all()) == 2

    def test_BL_010_007_15_clear(self) -> None:
        self.repo.save(self._make_role())
        self.repo.clear()
        assert self.repo.list_all() == []

    def test_BL_010_007_16_get_by_id_not_found(self) -> None:
        assert self.repo.get_by_id(RoleId("nope")) is None


class TestInMemoryPermissionRepository:
    def setup_method(self) -> None:
        self.repo = InMemoryPermissionRepository()

    def _make_perm(self, pid: str = "p1", name: str = "auth:user:read") -> Permission:
        return Permission(
            id=PermissionId(pid),
            name=PermissionName(name),
            resource="user",
            action="read",
            is_system=False,
            created_at=_NOW,
        )

    def test_BL_010_007_17_save_and_get_by_id(self) -> None:
        perm = self._make_perm()
        self.repo.save(perm)
        assert self.repo.get_by_id(PermissionId("p1")) is not None

    def test_BL_010_007_18_get_by_name(self) -> None:
        perm = self._make_perm()
        self.repo.save(perm)
        assert self.repo.get_by_name(PermissionName("auth:user:read")) is not None

    def test_BL_010_007_19_get_by_name_not_found(self) -> None:
        assert self.repo.get_by_name(PermissionName("auth:user:write")) is None

    def test_BL_010_007_20_list_all(self) -> None:
        self.repo.save(self._make_perm("p1", "auth:user:read"))
        self.repo.save(self._make_perm("p2", "auth:user:write"))
        assert len(self.repo.list_all()) == 2

    def test_BL_010_007_21_clear(self) -> None:
        self.repo.save(self._make_perm())
        self.repo.clear()
        assert self.repo.list_all() == []

    def test_BL_010_007_22_get_by_id_not_found(self) -> None:
        assert self.repo.get_by_id(PermissionId("nope")) is None


class TestInMemorySessionRepository:
    def setup_method(self) -> None:
        self.repo = InMemorySessionRepository()

    def _make_session(
        self,
        sid: str = "s1",
        uid: str = "u1",
        status: SessionStatus = SessionStatus.ACTIVE,
    ) -> Session:
        return Session(
            id=SessionId(sid),
            user_id=UserId(uid),
            refresh_token_id=TokenId("tok-1"),
            status=status,
            created_at=_NOW,
            expires_at=_EXPIRES,
        )

    def test_BL_010_007_23_save_and_get_by_id(self) -> None:
        session = self._make_session()
        self.repo.save(session)
        assert self.repo.get_by_id(SessionId("s1")) is not None

    def test_BL_010_007_24_get_active_by_user(self) -> None:
        self.repo.save(self._make_session("s1", "u1", SessionStatus.ACTIVE))
        self.repo.save(self._make_session("s2", "u1", SessionStatus.REVOKED))
        active = self.repo.get_active_by_user(UserId("u1"))
        assert len(active) == 1

    def test_BL_010_007_25_delete(self) -> None:
        self.repo.save(self._make_session())
        self.repo.delete(SessionId("s1"))
        assert self.repo.get_by_id(SessionId("s1")) is None

    def test_BL_010_007_26_delete_nonexistent(self) -> None:
        self.repo.delete(SessionId("nope"))

    def test_BL_010_007_27_clear(self) -> None:
        self.repo.save(self._make_session())
        self.repo.clear()
        assert self.repo.get_by_id(SessionId("s1")) is None

    def test_BL_010_007_28_get_by_id_not_found(self) -> None:
        assert self.repo.get_by_id(SessionId("nope")) is None

    def test_BL_020_004_1_get_by_refresh_token_id(self) -> None:
        self.repo.save(self._make_session())
        found = self.repo.get_by_refresh_token_id(TokenId("tok-1"))
        assert found is not None
        assert found.id == SessionId("s1")

    def test_BL_020_004_2_get_by_refresh_token_id_not_found(self) -> None:
        assert self.repo.get_by_refresh_token_id(TokenId("nope")) is None


class TestInMemoryAuditRepository:
    def setup_method(self) -> None:
        self.repo = InMemoryAuditRepository()

    def _make_event(
        self,
        eid: str = "e1",
        actor: str | None = "subj-1",
    ) -> AuditEvent:
        return AuditEvent(
            id=AuditEventId(eid),
            event_type=AuditEventType.LOGIN_SUCCESS,
            severity=AuditSeverity.INFO,
            created_at=_NOW,
            actor_subject=AuthSubject(actor) if actor else None,
        )

    def test_BL_010_007_29_save_and_list(self) -> None:
        self.repo.save(self._make_event())
        assert len(self.repo.all_events) == 1

    def test_BL_010_007_30_list_by_actor(self) -> None:
        self.repo.save(self._make_event("e1", "subj-1"))
        self.repo.save(self._make_event("e2", "subj-2"))
        result = self.repo.list_by_actor(AuthSubject("subj-1"))
        assert len(result) == 1

    def test_BL_010_007_31_clear(self) -> None:
        self.repo.save(self._make_event())
        self.repo.clear()
        assert self.repo.all_events == []

    def test_BL_010_007_32_list_by_actor_no_actor(self) -> None:
        self.repo.save(self._make_event("e1", None))
        result = self.repo.list_by_actor(AuthSubject("subj-1"))
        assert result == []
