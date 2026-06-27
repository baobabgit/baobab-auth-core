"""Tests de SessionPolicy."""

import dataclasses

from baobab_auth_core.domain.policies.session_policy import SessionPolicy


class TestSessionPolicy:
    def test_BL_010_004_1_defaults(self) -> None:
        p = SessionPolicy()
        assert p.access_token_ttl_seconds == 900
        assert p.refresh_token_ttl_seconds == 2592000
        assert p.max_failed_login_attempts == 5
        assert p.lockout_duration_seconds == 900
        assert p.revoke_other_sessions_on_password_change is True

    def test_BL_010_004_2_custom(self) -> None:
        p = SessionPolicy(
            access_token_ttl_seconds=60,
            max_failed_login_attempts=3,
            revoke_other_sessions_on_password_change=False,
        )
        assert p.access_token_ttl_seconds == 60
        assert p.max_failed_login_attempts == 3
        assert p.revoke_other_sessions_on_password_change is False

    def test_BL_010_004_3_frozen(self) -> None:
        import pytest

        p = SessionPolicy()
        with pytest.raises(dataclasses.FrozenInstanceError):
            p.access_token_ttl_seconds = 0  # type: ignore[misc]
