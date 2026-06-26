"""Utilitaires de test de baobab-auth-core (fakes in-memory).

:spec: BL-010-007
"""

from baobab_auth_core.testing.fake_clock import FakeClock as FakeClock
from baobab_auth_core.testing.fake_id_generator import (
    FakeIdGenerator as FakeIdGenerator,
)
from baobab_auth_core.testing.fake_password_hasher import (
    FakePasswordHasher as FakePasswordHasher,
)
from baobab_auth_core.testing.fake_token_provider import (
    FakeTokenProvider as FakeTokenProvider,
)
from baobab_auth_core.testing.in_memory_audit_repository import (
    InMemoryAuditRepository as InMemoryAuditRepository,
)
from baobab_auth_core.testing.in_memory_permission_repository import (
    InMemoryPermissionRepository as InMemoryPermissionRepository,
)
from baobab_auth_core.testing.in_memory_role_repository import (
    InMemoryRoleRepository as InMemoryRoleRepository,
)
from baobab_auth_core.testing.in_memory_session_repository import (
    InMemorySessionRepository as InMemorySessionRepository,
)
from baobab_auth_core.testing.in_memory_unit_of_work import (
    InMemoryUnitOfWork as InMemoryUnitOfWork,
)
from baobab_auth_core.testing.in_memory_user_repository import (
    InMemoryUserRepository as InMemoryUserRepository,
)

__all__ = [
    "FakeClock",
    "FakeIdGenerator",
    "FakePasswordHasher",
    "FakeTokenProvider",
    "InMemoryAuditRepository",
    "InMemoryPermissionRepository",
    "InMemoryRoleRepository",
    "InMemorySessionRepository",
    "InMemoryUnitOfWork",
    "InMemoryUserRepository",
]
