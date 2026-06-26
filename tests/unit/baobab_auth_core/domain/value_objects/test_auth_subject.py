"""Tests du value object AuthSubject."""

import dataclasses

import pytest

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.exceptions.validation import ValidationError


class TestAuthSubject:
    def test_BL_010_002_1_valid(self) -> None:
        s = AuthSubject("subj-123")
        assert s.value == "subj-123"

    def test_BL_010_002_2_raises_on_empty(self) -> None:
        with pytest.raises(ValidationError):
            AuthSubject("")

    def test_BL_010_002_3_raises_on_whitespace(self) -> None:
        with pytest.raises(ValidationError):
            AuthSubject("   ")

    def test_BL_010_002_4_equality(self) -> None:
        assert AuthSubject("x") == AuthSubject("x")
        assert AuthSubject("x") != AuthSubject("y")

    def test_BL_010_002_5_str(self) -> None:
        assert str(AuthSubject("s1")) == "s1"

    def test_BL_010_002_6_repr(self) -> None:
        assert "s1" in repr(AuthSubject("s1"))

    def test_BL_010_002_7_frozen(self) -> None:
        s = AuthSubject("abc")
        with pytest.raises(dataclasses.FrozenInstanceError):
            s.value = "xyz"  # type: ignore[misc]
