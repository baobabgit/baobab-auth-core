"""Tests du DTO AuthenticatedUser.

:spec: BL-020-007
"""

from datetime import UTC, datetime

from baobab_auth_core.application.results.authenticated_user import AuthenticatedUser
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestAuthenticatedUser:
    def test_BL_020_007_1_from_user_sans_secret(self) -> None:
        user = User(
            id=UserId("u1"),
            auth_subject=AuthSubject("subj-1"),
            email=Email("alice@example.com"),
            password_hash=PasswordHash("hashed:secret"),
            status=UserStatus.ACTIVE,
            role_names=(RoleName("USER"),),
            created_at=_NOW,
            updated_at=_NOW,
        )
        dto = AuthenticatedUser.from_user(user)
        assert dto.email == Email("alice@example.com")
        assert dto.status == UserStatus.ACTIVE
        assert dto.role_names == (RoleName("USER"),)
        assert not hasattr(dto, "password_hash")
        assert "hashed:secret" not in repr(dto)
