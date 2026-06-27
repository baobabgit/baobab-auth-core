"""Tests du value object Email."""

import dataclasses

import pytest

from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.exceptions.validation import InvalidEmailError


class TestEmail:
    def test_BL_010_002_1_normalize_lowercase(self) -> None:
        email = Email("Alice@Example.COM")
        assert email.value == "alice@example.com"

    def test_BL_010_002_2_strip_whitespace(self) -> None:
        email = Email("  alice@example.com  ")
        assert email.value == "alice@example.com"

    def test_BL_010_002_3_raises_on_empty(self) -> None:
        with pytest.raises(InvalidEmailError):
            Email("")

    def test_BL_010_002_4_raises_on_whitespace_only(self) -> None:
        with pytest.raises(InvalidEmailError):
            Email("   ")

    def test_BL_010_002_5_raises_on_no_at_sign(self) -> None:
        with pytest.raises(InvalidEmailError):
            Email("notanemail")

    def test_BL_010_002_6_equality_by_value(self) -> None:
        assert Email("alice@example.com") == Email("ALICE@EXAMPLE.COM")

    def test_BL_010_002_7_str_returns_value(self) -> None:
        assert str(Email("a@b.com")) == "a@b.com"

    def test_BL_010_002_8_repr_contains_value(self) -> None:
        assert "a@b.com" in repr(Email("a@b.com"))

    def test_BL_010_002_9_frozen(self) -> None:
        email = Email("alice@example.com")
        with pytest.raises(dataclasses.FrozenInstanceError):
            email.value = "bob@example.com"  # type: ignore[misc]

    def test_BL_010_002_10_hash_for_dict_key(self) -> None:
        d = {Email("a@b.com"): 1}
        assert d[Email("A@B.COM")] == 1
