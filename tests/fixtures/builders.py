"""Builders de fixtures partagés entre les tests.

:spec: BL-010-008
"""

from datetime import UTC, datetime

from baobab_auth_core.domain.entities.audit_event import AuditEvent
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.entities.user_profile import UserProfile
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

_NOW = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)
_EXPIRES = datetime(2024, 2, 1, 0, 0, 0, tzinfo=UTC)


def make_user(
    user_id: str = "user-1",
    email: str = "alice@example.com",
    subject: str = "subj-1",
    status: UserStatus = UserStatus.ACTIVE,
) -> User:
    """Construit un User de test avec des valeurs par défaut."""
    return User(
        id=UserId(user_id),
        auth_subject=AuthSubject(subject),
        email=Email(email),
        password_hash=PasswordHash("hashed:secret"),
        status=status,
        role_names=(RoleName("USER"),),
        created_at=_NOW,
        updated_at=_NOW,
    )


def make_role(
    role_id: str = "role-1",
    name: str = "USER",
) -> Role:
    """Construit un Role de test."""
    return Role(
        id=RoleId(role_id),
        name=RoleName(name),
        is_system=False,
        created_at=_NOW,
        updated_at=_NOW,
    )


def make_permission(
    perm_id: str = "perm-1",
    name: str = "auth:user:read",
) -> Permission:
    """Construit une Permission de test."""
    return Permission(
        id=PermissionId(perm_id),
        name=PermissionName(name),
        resource="user",
        action="read",
        is_system=False,
        created_at=_NOW,
    )


def make_session(
    session_id: str = "sess-1",
    user_id: str = "user-1",
    status: SessionStatus = SessionStatus.ACTIVE,
) -> Session:
    """Construit une Session de test."""
    return Session(
        id=SessionId(session_id),
        user_id=UserId(user_id),
        refresh_token_id=TokenId("tok-1"),
        status=status,
        created_at=_NOW,
        expires_at=_EXPIRES,
    )


def make_audit_event(
    event_id: str = "evt-1",
    event_type: AuditEventType = AuditEventType.LOGIN_SUCCESS,
) -> AuditEvent:
    """Construit un AuditEvent de test."""
    return AuditEvent(
        id=AuditEventId(event_id),
        event_type=event_type,
        severity=AuditSeverity.INFO,
        created_at=_NOW,
        actor_subject=AuthSubject("subj-1"),
    )


def make_user_profile(user_id: str = "user-1") -> UserProfile:
    """Construit un UserProfile de test."""
    return UserProfile(
        user_id=UserId(user_id),
        created_at=_NOW,
        updated_at=_NOW,
        display_name="Alice",
    )
