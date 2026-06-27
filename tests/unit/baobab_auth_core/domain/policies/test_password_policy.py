"""Tests de PasswordPolicy."""

import pytest

from baobab_auth_core.domain.policies.password_policy import PasswordPolicy
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
from baobab_auth_core.exceptions.validation import WeakPasswordError


class TestPasswordPolicy:
    def setup_method(self) -> None:
        self.policy = PasswordPolicy()

    def test_BL_010_004_1_defaults(self) -> None:
        assert self.policy.min_length == 12
        assert self.policy.max_length == 256
        assert self.policy.require_letter is True
        assert self.policy.require_digit_or_symbol is True
        assert self.policy.forbid_email_as_password is True

    def test_BL_010_004_2_valid_password(self) -> None:
        self.policy.validate(PlainPassword("Secure!Password1"))

    def test_BL_010_004_3_too_short(self) -> None:
        with pytest.raises(WeakPasswordError, match="12"):
            self.policy.validate(PlainPassword("Short1!"))

    def test_BL_010_004_4_too_long(self) -> None:
        policy = PasswordPolicy(max_length=10)
        with pytest.raises(WeakPasswordError, match="10"):
            policy.validate(PlainPassword("VeryLongPassword1!"))

    def test_BL_010_004_5_no_letter(self) -> None:
        with pytest.raises(WeakPasswordError, match="lettre"):
            self.policy.validate(PlainPassword("123456789012"))

    def test_BL_010_004_6_no_digit_or_symbol(self) -> None:
        with pytest.raises(WeakPasswordError, match="chiffre"):
            self.policy.validate(PlainPassword("AbcdefghijkL"))

    def test_BL_010_004_7_email_as_password(self) -> None:
        email = Email("alice@example.com")
        with pytest.raises(WeakPasswordError, match="email"):
            self.policy.validate(PlainPassword("alice@example.com"), email=email)

    def test_BL_010_004_8_email_as_password_case_insensitive(self) -> None:
        email = Email("alice@example.com")
        with pytest.raises(WeakPasswordError):
            self.policy.validate(PlainPassword("ALICE@EXAMPLE.COM"), email=email)

    def test_BL_010_004_9_email_check_skipped_when_none(self) -> None:
        self.policy.validate(PlainPassword("Secure!Pass123"), email=None)

    def test_BL_010_004_10_custom_policy(self) -> None:
        policy = PasswordPolicy(
            min_length=4,
            max_length=20,
            require_letter=False,
            require_digit_or_symbol=False,
            forbid_email_as_password=False,
        )
        policy.validate(PlainPassword("abcd"))

    def test_BL_010_004_11_has_digit(self) -> None:
        policy = PasswordPolicy(require_digit_or_symbol=True)
        policy.validate(PlainPassword("Abcdefghijkl1"))

    def test_BL_010_004_12_has_symbol(self) -> None:
        policy = PasswordPolicy(require_digit_or_symbol=True)
        policy.validate(PlainPassword("Abcdefghijkl!"))
