"""baobab-auth-core — socle métier d'authentification et d'autorisation.

Version : 0.5.1

Ce package expose une **API publique stable** (entités, value objects, enums,
policies, catalogue, ports, DTO et cas d'usage) destinée aux briques
``database``, ``security``, ``api``, ``client`` et ``admin``. Il ne contient
aucune dépendance sur des technologies concrètes (ORM, framework web, JWT,
Argon2, etc.).

:spec: BL-010-001, BL-050-001
"""

from baobab_auth_core.application.results.auth_context import AuthContext
from baobab_auth_core.application.results.authenticated_user import AuthenticatedUser
from baobab_auth_core.application.results.session_dto import SessionDTO
from baobab_auth_core.application.results.token_claims import TokenClaims
from baobab_auth_core.application.results.token_issue_context import TokenIssueContext
from baobab_auth_core.application.results.token_pair import TokenPair
from baobab_auth_core.application.use_cases.assign_role import AssignRole
from baobab_auth_core.application.use_cases.authenticate_user import AuthenticateUser
from baobab_auth_core.application.use_cases.bootstrap_super_admin import (
    BootstrapSuperAdmin,
)
from baobab_auth_core.application.use_cases.change_password import ChangePassword
from baobab_auth_core.application.use_cases.disable_user import DisableUser
from baobab_auth_core.application.use_cases.enable_user import EnableUser
from baobab_auth_core.application.use_cases.get_current_user import GetCurrentUser
from baobab_auth_core.application.use_cases.get_user_by_subject import GetUserBySubject
from baobab_auth_core.application.use_cases.list_permissions import ListPermissions
from baobab_auth_core.application.use_cases.list_roles import ListRoles
from baobab_auth_core.application.use_cases.list_user_sessions import ListUserSessions
from baobab_auth_core.application.use_cases.logout import Logout
from baobab_auth_core.application.use_cases.refresh_session import RefreshSession
from baobab_auth_core.application.use_cases.register_user import RegisterUser
from baobab_auth_core.application.use_cases.remove_role import RemoveRole
from baobab_auth_core.application.use_cases.request_jwk_rotation import (
    RequestJwkRotation,
)
from baobab_auth_core.application.use_cases.revoke_all_sessions import RevokeAllSessions
from baobab_auth_core.application.use_cases.revoke_session import RevokeSession
from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog
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
from baobab_auth_core.domain.policies.lockout_policy import LockoutPolicy
from baobab_auth_core.domain.policies.password_policy import PasswordPolicy
from baobab_auth_core.domain.policies.permission_policy import PermissionPolicy
from baobab_auth_core.domain.policies.role_policy import RolePolicy
from baobab_auth_core.domain.policies.session_policy import SessionPolicy
from baobab_auth_core.domain.value_objects.audit_event_id import AuditEventId
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.password_hasher import PasswordHasher
from baobab_auth_core.ports.permission_repository import PermissionRepository
from baobab_auth_core.ports.role_repository import RoleRepository
from baobab_auth_core.ports.session_repository import SessionRepository
from baobab_auth_core.ports.token_provider import TokenProvider
from baobab_auth_core.ports.unit_of_work import UnitOfWork
from baobab_auth_core.ports.user_repository import UserRepository

__version__ = "0.5.1"

__all__ = [
    # Use cases
    "AssignRole",
    # Entités
    "AuditEvent",
    # Value objects
    "AuditEventId",
    # Enums
    "AuditEventType",
    # Ports
    "AuditRepository",
    "AuditSeverity",
    # DTO
    "AuthContext",
    "AuthSubject",
    "AuthenticateUser",
    "AuthenticatedUser",
    "BootstrapSuperAdmin",
    "ChangePassword",
    "Clock",
    # Catalogues
    "DefaultAuthCatalog",
    "DisableUser",
    "Email",
    "EnableUser",
    "GetCurrentUser",
    "GetUserBySubject",
    "IdGenerator",
    "ListPermissions",
    "ListRoles",
    "ListUserSessions",
    # Policies
    "LockoutPolicy",
    "Logout",
    "PasswordHash",
    "PasswordHasher",
    "PasswordPolicy",
    "Permission",
    "PermissionId",
    "PermissionName",
    "PermissionPolicy",
    "PermissionRepository",
    "PlainPassword",
    "RefreshSession",
    "RegisterUser",
    "RemoveRole",
    "RequestJwkRotation",
    "RevokeAllSessions",
    "RevokeSession",
    "Role",
    "RoleId",
    "RoleName",
    "RolePolicy",
    "RoleRepository",
    "Session",
    "SessionDTO",
    "SessionId",
    "SessionPolicy",
    "SessionRepository",
    "SessionStatus",
    "TokenClaims",
    "TokenId",
    "TokenIssueContext",
    "TokenPair",
    "TokenProvider",
    "UnitOfWork",
    "User",
    "UserId",
    "UserProfile",
    "UserRepository",
    "UserStatus",
    "__version__",
]
