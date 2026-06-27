"""Ports (protocoles) de baobab-auth-core.

:spec: BL-010-006
"""

from baobab_auth_core.ports.audit_repository import AuditRepository as AuditRepository
from baobab_auth_core.ports.clock import Clock as Clock
from baobab_auth_core.ports.id_generator import IdGenerator as IdGenerator
from baobab_auth_core.ports.password_hasher import PasswordHasher as PasswordHasher
from baobab_auth_core.ports.permission_repository import (
    PermissionRepository as PermissionRepository,
)
from baobab_auth_core.ports.role_repository import RoleRepository as RoleRepository
from baobab_auth_core.ports.session_repository import (
    SessionRepository as SessionRepository,
)
from baobab_auth_core.ports.token_provider import TokenProvider as TokenProvider
from baobab_auth_core.ports.unit_of_work import UnitOfWork as UnitOfWork
from baobab_auth_core.ports.user_repository import UserRepository as UserRepository

__all__ = [
    "AuditRepository",
    "Clock",
    "IdGenerator",
    "PasswordHasher",
    "PermissionRepository",
    "RoleRepository",
    "SessionRepository",
    "TokenProvider",
    "UnitOfWork",
    "UserRepository",
]
