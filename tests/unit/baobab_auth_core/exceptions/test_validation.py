"""Tests des exceptions de validation."""

import pytest

from baobab_auth_core.exceptions.base import BaobabAuthCoreError
from baobab_auth_core.exceptions.validation import (
    InvalidEmailError,
    InvalidPermissionNameError,
    InvalidRoleNameError,
    ValidationError,
    WeakPasswordError,
)


class TestValidationError:
    def test_BL_010_005_1_hierarchy(self) -> None:
        assert issubclass(ValidationError, BaobabAuthCoreError)

    def test_BL_010_005_2_can_raise(self) -> None:
        with pytest.raises(ValidationError):
            raise ValidationError("invalid")


class TestInvalidEmailError:
    def test_BL_010_005_3_hierarchy(self) -> None:
        assert issubclass(InvalidEmailError, ValidationError)

    def test_BL_010_005_4_message(self) -> None:
        err = InvalidEmailError("bad email")
        assert "bad email" in str(err)


class TestWeakPasswordError:
    def test_BL_010_005_5_hierarchy(self) -> None:
        assert issubclass(WeakPasswordError, ValidationError)


class TestInvalidRoleNameError:
    def test_BL_010_005_6_hierarchy(self) -> None:
        assert issubclass(InvalidRoleNameError, ValidationError)


class TestInvalidPermissionNameError:
    def test_BL_010_005_7_hierarchy(self) -> None:
        assert issubclass(InvalidPermissionNameError, ValidationError)

    def test_BL_010_005_8_can_raise(self) -> None:
        with pytest.raises(InvalidPermissionNameError):
            raise InvalidPermissionNameError("bad format")
