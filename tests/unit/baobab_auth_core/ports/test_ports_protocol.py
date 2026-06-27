"""Tests de conformité des fakes aux protocoles de ports.

Vérifie que chaque fake implémente correctement le protocole correspondant.

:spec: BL-010-006
"""

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
from baobab_auth_core.testing.fake_clock import FakeClock
from baobab_auth_core.testing.fake_id_generator import FakeIdGenerator
from baobab_auth_core.testing.fake_password_hasher import FakePasswordHasher
from baobab_auth_core.testing.fake_token_provider import FakeTokenProvider
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


class TestPortsProtocolCompliance:
    def test_BL_010_006_1_fake_clock_is_clock(self) -> None:
        assert isinstance(FakeClock(), Clock)

    def test_BL_010_006_2_fake_id_generator_is_id_generator(self) -> None:
        assert isinstance(FakeIdGenerator(), IdGenerator)

    def test_BL_010_006_3_fake_password_hasher_is_password_hasher(self) -> None:
        assert isinstance(FakePasswordHasher(), PasswordHasher)

    def test_BL_010_006_4_fake_token_provider_is_token_provider(self) -> None:
        assert isinstance(FakeTokenProvider(), TokenProvider)

    def test_BL_010_006_5_in_memory_user_repo_is_user_repository(self) -> None:
        assert isinstance(InMemoryUserRepository(), UserRepository)

    def test_BL_010_006_6_in_memory_role_repo_is_role_repository(self) -> None:
        assert isinstance(InMemoryRoleRepository(), RoleRepository)

    def test_BL_010_006_7_in_memory_permission_repo_is_permission_repository(
        self,
    ) -> None:
        assert isinstance(InMemoryPermissionRepository(), PermissionRepository)

    def test_BL_010_006_8_in_memory_session_repo_is_session_repository(self) -> None:
        assert isinstance(InMemorySessionRepository(), SessionRepository)

    def test_BL_010_006_9_in_memory_audit_repo_is_audit_repository(self) -> None:
        assert isinstance(InMemoryAuditRepository(), AuditRepository)

    def test_BL_010_006_10_in_memory_uow_is_unit_of_work(self) -> None:
        assert isinstance(InMemoryUnitOfWork(), UnitOfWork)
