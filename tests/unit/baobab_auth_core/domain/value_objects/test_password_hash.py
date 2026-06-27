"""Tests du value object PasswordHash."""

import dataclasses

import pytest

from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.exceptions.validation import ValidationError


class TestPasswordHash:
    def test_BL_010_002_1_valid(self) -> None:
        h = PasswordHash("$argon2id$v=19$...")
        assert h.value == "$argon2id$v=19$..."

    def test_BL_010_002_2_raises_on_empty(self) -> None:
        with pytest.raises(ValidationError):
            PasswordHash("")

    def test_BL_010_002_3_str_masked(self) -> None:
        h = PasswordHash("$argon2id$secret")
        assert "argon" not in str(h)
        assert str(h) == "***"

    def test_BL_010_002_4_repr_masked(self) -> None:
        h = PasswordHash("$argon2id$secret")
        assert "argon" not in repr(h)
        assert "***" in repr(h)

    def test_BL_010_002_5_equality(self) -> None:
        assert PasswordHash("abc") == PasswordHash("abc")
        assert PasswordHash("abc") != PasswordHash("xyz")

    def test_BL_010_002_6_frozen(self) -> None:
        h = PasswordHash("abc")
        with pytest.raises(dataclasses.FrozenInstanceError):
            h.value = "xyz"  # type: ignore[misc]
