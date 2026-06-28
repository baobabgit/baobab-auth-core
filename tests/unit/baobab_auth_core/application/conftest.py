"""Fixtures partagées des tests de la couche application v0.2.0."""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.testing.fake_clock import FakeClock
from baobab_auth_core.testing.fake_id_generator import FakeIdGenerator
from baobab_auth_core.testing.fake_password_hasher import FakePasswordHasher
from baobab_auth_core.testing.fake_token_provider import FakeTokenProvider
from baobab_auth_core.testing.in_memory_audit_repository import InMemoryAuditRepository
from baobab_auth_core.testing.in_memory_session_repository import (
    InMemorySessionRepository,
)
from baobab_auth_core.testing.in_memory_unit_of_work import InMemoryUnitOfWork
from baobab_auth_core.testing.in_memory_user_repository import InMemoryUserRepository

VALID_PASSWORD = "Sup3rSecret!!"
VALID_EMAIL = "alice@example.com"


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock(datetime(2024, 1, 1, tzinfo=UTC))


@pytest.fixture
def ids() -> FakeIdGenerator:
    return FakeIdGenerator()


@pytest.fixture
def users() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def sessions() -> InMemorySessionRepository:
    return InMemorySessionRepository()


@pytest.fixture
def audit() -> InMemoryAuditRepository:
    return InMemoryAuditRepository()


@pytest.fixture
def hasher() -> FakePasswordHasher:
    return FakePasswordHasher()


@pytest.fixture
def tokens() -> FakeTokenProvider:
    return FakeTokenProvider()


@pytest.fixture
def uow() -> InMemoryUnitOfWork:
    return InMemoryUnitOfWork()


@pytest.fixture
def valid_email() -> str:
    return VALID_EMAIL


@pytest.fixture
def valid_password() -> str:
    return VALID_PASSWORD


def _build_user(
    hasher: FakePasswordHasher,
    *,
    email: str = VALID_EMAIL,
    password: str = VALID_PASSWORD,
    subject: str = "subj-alice",
    user_id: str = "user-alice",
    status: UserStatus = UserStatus.ACTIVE,
) -> User:
    """Construit un User au mot de passe connu (hash via le fake)."""
    from baobab_auth_core.domain.value_objects.plain_password import PlainPassword

    now = datetime(2024, 1, 1, tzinfo=UTC)
    return User(
        id=UserId(user_id),
        auth_subject=AuthSubject(subject),
        email=Email(email),
        password_hash=hasher.hash(PlainPassword(password)),
        status=status,
        role_names=(RoleName("USER"),),
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def make_active_user(hasher: FakePasswordHasher):  # type: ignore[no-untyped-def]
    """Factory de User (mot de passe connu) injectable dans les tests."""

    def _factory(**kwargs: object) -> User:
        return _build_user(hasher, **kwargs)  # type: ignore[arg-type]

    return _factory
