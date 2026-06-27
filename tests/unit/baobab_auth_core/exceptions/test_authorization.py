"""Tests des exceptions d'autorisation."""

import pytest

from baobab_auth_core.exceptions.authorization import (
    AuthorizationError,
    ForbiddenError,
    PermissionDeniedError,
)
from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class TestAuthorizationExceptions:
    def test_BL_010_005_1_authorization_inherits_base(self) -> None:
        assert issubclass(AuthorizationError, BaobabAuthCoreError)

    def test_BL_010_005_2_forbidden_inherits_authorization(self) -> None:
        assert issubclass(ForbiddenError, AuthorizationError)

    def test_BL_010_005_3_permission_denied_inherits_authorization(self) -> None:
        assert issubclass(PermissionDeniedError, AuthorizationError)

    def test_BL_010_005_4_forbidden_can_raise(self) -> None:
        with pytest.raises(ForbiddenError):
            raise ForbiddenError("forbidden")

    def test_BL_010_005_5_permission_denied(self) -> None:
        with pytest.raises(PermissionDeniedError):
            raise PermissionDeniedError("denied")

    def test_BL_010_005_6_authorization_error(self) -> None:
        with pytest.raises(AuthorizationError):
            raise AuthorizationError("auth error")
