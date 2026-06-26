"""Tests des exceptions de session."""

import pytest

from baobab_auth_core.exceptions.base import BaobabAuthCoreError
from baobab_auth_core.exceptions.session import (
    SessionExpiredError,
    SessionNotFoundError,
    SessionRevokedError,
)


class TestSessionExceptions:
    def test_BL_010_005_1_all_inherit_base(self) -> None:
        for cls in (SessionNotFoundError, SessionExpiredError, SessionRevokedError):
            assert issubclass(cls, BaobabAuthCoreError)

    def test_BL_010_005_2_session_not_found(self) -> None:
        with pytest.raises(SessionNotFoundError):
            raise SessionNotFoundError("not found")

    def test_BL_010_005_3_session_expired(self) -> None:
        with pytest.raises(SessionExpiredError):
            raise SessionExpiredError("expired")

    def test_BL_010_005_4_session_revoked(self) -> None:
        with pytest.raises(SessionRevokedError):
            raise SessionRevokedError("revoked")
