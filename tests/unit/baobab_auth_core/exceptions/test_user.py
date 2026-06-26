"""Tests des exceptions utilisateur."""

import pytest

from baobab_auth_core.exceptions.base import BaobabAuthCoreError
from baobab_auth_core.exceptions.user import (
    UserAlreadyExistsError,
    UserDeletedError,
    UserDisabledError,
    UserLockedError,
    UserNotFoundError,
)


class TestUserExceptions:
    def test_BL_010_005_1_all_inherit_base(self) -> None:
        for cls in (
            UserAlreadyExistsError,
            UserNotFoundError,
            UserDisabledError,
            UserLockedError,
            UserDeletedError,
        ):
            assert issubclass(cls, BaobabAuthCoreError)

    def test_BL_010_005_2_user_not_found(self) -> None:
        with pytest.raises(UserNotFoundError, match="alice"):
            raise UserNotFoundError("alice not found")

    def test_BL_010_005_3_user_locked(self) -> None:
        err = UserLockedError("locked until 2025")
        assert "locked" in str(err).lower()

    def test_BL_010_005_4_user_already_exists(self) -> None:
        with pytest.raises(UserAlreadyExistsError):
            raise UserAlreadyExistsError("already exists")

    def test_BL_010_005_5_user_disabled(self) -> None:
        with pytest.raises(UserDisabledError):
            raise UserDisabledError("disabled")

    def test_BL_010_005_6_user_deleted(self) -> None:
        with pytest.raises(UserDeletedError):
            raise UserDeletedError("deleted")
