"""Tests du value object PlainPassword."""

import dataclasses

import pytest

from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
from baobab_auth_core.exceptions.validation import ValidationError


class TestPlainPassword:
    def test_BL_010_002_1_valid(self) -> None:
        p = PlainPassword("secret123!")
        assert p.value == "secret123!"

    def test_BL_010_002_2_raises_on_empty(self) -> None:
        with pytest.raises(ValidationError):
            PlainPassword("")

    def test_BL_010_002_3_str_masked(self) -> None:
        p = PlainPassword("secret123!")
        assert "secret" not in str(p)
        assert str(p) == "***"

    def test_BL_010_002_4_repr_masked(self) -> None:
        p = PlainPassword("secret123!")
        assert "secret" not in repr(p)
        assert "***" in repr(p)

    def test_BL_010_002_5_equality(self) -> None:
        assert PlainPassword("abc") == PlainPassword("abc")
        assert PlainPassword("abc") != PlainPassword("xyz")

    def test_BL_010_002_6_frozen(self) -> None:
        p = PlainPassword("abc")
        with pytest.raises(dataclasses.FrozenInstanceError):
            p.value = "xyz"  # type: ignore[misc]
