"""Tests des exceptions d'authentification."""

import pytest

from baobab_auth_core.exceptions.auth import (
    InvalidCredentialsError,
    TokenExpiredError,
    TokenInvalidError,
)
from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class TestAuthExceptions:
    def test_BL_010_005_1_all_inherit_base(self) -> None:
        for cls in (InvalidCredentialsError, TokenInvalidError, TokenExpiredError):
            assert issubclass(cls, BaobabAuthCoreError)

    def test_BL_010_005_2_invalid_credentials(self) -> None:
        with pytest.raises(InvalidCredentialsError):
            raise InvalidCredentialsError("invalid credentials")

    def test_BL_010_005_3_token_invalid(self) -> None:
        with pytest.raises(TokenInvalidError):
            raise TokenInvalidError("bad signature")

    def test_BL_010_005_4_token_expired(self) -> None:
        with pytest.raises(TokenExpiredError):
            raise TokenExpiredError("token expired")
