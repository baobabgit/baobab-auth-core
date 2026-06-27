"""Tests du value object RoleName."""

import dataclasses

import pytest

from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.exceptions.validation import InvalidRoleNameError


class TestRoleName:
    def test_BL_010_002_1_valid_uppercase(self) -> None:
        r = RoleName("USER")
        assert r.value == "USER"

    def test_BL_010_002_2_normalize_uppercase(self) -> None:
        r = RoleName("user")
        assert r.value == "USER"

    def test_BL_010_002_3_raises_on_empty(self) -> None:
        with pytest.raises(InvalidRoleNameError):
            RoleName("")

    def test_BL_010_002_4_raises_on_whitespace_only(self) -> None:
        with pytest.raises(InvalidRoleNameError):
            RoleName("   ")

    def test_BL_010_002_5_raises_on_spaces_in_name(self) -> None:
        with pytest.raises(InvalidRoleNameError):
            RoleName("SUPER ADMIN")

    def test_BL_010_002_6_equality(self) -> None:
        assert RoleName("USER") == RoleName("user")

    def test_BL_010_002_7_str(self) -> None:
        assert str(RoleName("admin")) == "ADMIN"

    def test_BL_010_002_8_repr(self) -> None:
        assert "ADMIN" in repr(RoleName("ADMIN"))

    def test_BL_010_002_9_frozen(self) -> None:
        r = RoleName("USER")
        with pytest.raises(dataclasses.FrozenInstanceError):
            r.value = "ADMIN"  # type: ignore[misc]
