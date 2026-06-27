"""Tests de l'entité User."""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.validation import ValidationError

_NOW = datetime(2024, 1, 1, tzinfo=UTC)
_LATER = datetime(2024, 6, 1, tzinfo=UTC)


def _make_user(status: UserStatus = UserStatus.ACTIVE, **kwargs: object) -> User:
    defaults: dict[str, object] = dict(
        id=UserId("u1"),
        auth_subject=AuthSubject("s1"),
        email=Email("alice@example.com"),
        password_hash=PasswordHash("hashed"),
        status=status,
        role_names=(RoleName("USER"),),
        created_at=_NOW,
        updated_at=_NOW,
    )
    defaults.update(kwargs)
    return User(**defaults)  # type: ignore[arg-type]


class TestUser:
    def test_BL_010_003_1_construction(self) -> None:
        user = _make_user()
        assert user.id == UserId("u1")
        assert user.email == Email("alice@example.com")
        assert user.status == UserStatus.ACTIVE

    def test_BL_010_003_2_raises_on_negative_failed_count(self) -> None:
        with pytest.raises(ValidationError):
            _make_user(failed_login_count=-1)

    def test_BL_010_003_3_raises_on_duplicate_roles(self) -> None:
        with pytest.raises(ValidationError):
            _make_user(role_names=(RoleName("USER"), RoleName("USER")))

    def test_BL_010_003_4_activate(self) -> None:
        user = _make_user(status=UserStatus.PENDING)
        user.activate(_LATER)
        assert user.status == UserStatus.ACTIVE
        assert user.updated_at == _LATER

    def test_BL_010_003_5_disable(self) -> None:
        user = _make_user()
        user.disable(_LATER)
        assert user.status == UserStatus.DISABLED

    def test_BL_010_003_6_lock(self) -> None:
        user = _make_user()
        user.lock(_LATER, _NOW)
        assert user.status == UserStatus.LOCKED
        assert user.locked_until == _LATER

    def test_BL_010_003_7_unlock(self) -> None:
        user = _make_user(
            status=UserStatus.LOCKED,
            failed_login_count=3,
            locked_until=_LATER,
        )
        user.unlock(_NOW)
        assert user.status == UserStatus.ACTIVE
        assert user.failed_login_count == 0
        assert user.locked_until is None

    def test_BL_010_003_8_mark_login_success(self) -> None:
        user = _make_user(failed_login_count=2)
        user.mark_login_success(_LATER)
        assert user.last_login_at == _LATER
        assert user.failed_login_count == 0

    def test_BL_010_003_9_mark_login_failure(self) -> None:
        user = _make_user()
        user.mark_login_failure(_NOW)
        assert user.failed_login_count == 1

    def test_BL_010_003_10_change_password_hash(self) -> None:
        user = _make_user()
        new_hash = PasswordHash("new_hash")
        user.change_password_hash(new_hash, _LATER)
        assert user.password_hash == new_hash
        assert user.updated_at == _LATER

    def test_BL_010_003_11_assign_role_no_duplicate(self) -> None:
        user = _make_user()
        user.assign_role(RoleName("ADMIN"), _LATER)
        assert RoleName("ADMIN") in user.role_names
        user.assign_role(RoleName("ADMIN"), _LATER)
        assert user.role_names.count(RoleName("ADMIN")) == 1

    def test_BL_010_003_12_remove_role(self) -> None:
        user = _make_user(role_names=(RoleName("USER"), RoleName("ADMIN")))
        user.remove_role(RoleName("ADMIN"), _LATER)
        assert RoleName("ADMIN") not in user.role_names

    def test_BL_010_003_13_remove_nonexistent_role_no_error(self) -> None:
        user = _make_user()
        user.remove_role(RoleName("ADMIN"), _LATER)
        assert user.role_names == (RoleName("USER"),)

    def test_BL_010_003_14_has_role(self) -> None:
        user = _make_user()
        assert user.has_role(RoleName("USER")) is True
        assert user.has_role(RoleName("ADMIN")) is False

    def test_BL_010_003_15_repr_no_secret(self) -> None:
        user = _make_user()
        r = repr(user.password_hash)
        assert "hashed" not in r
        s = str(user.password_hash)
        assert "hashed" not in s

    def test_BL_010_003_16_assign_role_updates_updated_at(self) -> None:
        user = _make_user()
        user.assign_role(RoleName("ADMIN"), _LATER)
        assert user.updated_at == _LATER
