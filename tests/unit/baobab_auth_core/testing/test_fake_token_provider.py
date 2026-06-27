"""Tests du FakeTokenProvider."""

import pytest

from baobab_auth_core.exceptions.auth import TokenExpiredError, TokenInvalidError
from baobab_auth_core.testing.fake_token_provider import FakeTokenProvider


class TestFakeTokenProvider:
    def setup_method(self) -> None:
        self.provider = FakeTokenProvider()

    def test_BL_010_007_1_generate_token_id(self) -> None:
        tid = self.provider.generate_token_id()
        assert tid.value.startswith("token-id-")

    def test_BL_010_007_2_token_id_increments(self) -> None:
        t1 = self.provider.generate_token_id()
        t2 = self.provider.generate_token_id()
        assert t1 != t2

    def test_BL_010_007_3_create_access_token(self) -> None:
        token = self.provider.create_access_token("subj-1", 900)
        assert "subj-1" in token

    def test_BL_010_007_4_verify_valid_token(self) -> None:
        token = self.provider.create_access_token("subj-1", 900)
        payload = self.provider.verify_access_token(token)
        assert payload["sub"] == "subj-1"

    def test_BL_010_007_5_verify_expired_token(self) -> None:
        with pytest.raises(TokenExpiredError):
            self.provider.verify_access_token("fake-token:EXPIRED")

    def test_BL_010_007_6_verify_invalid_token(self) -> None:
        with pytest.raises(TokenInvalidError):
            self.provider.verify_access_token("not-a-fake-token")

    def test_BL_010_007_7_verify_invalid_marker(self) -> None:
        with pytest.raises(TokenInvalidError):
            self.provider.verify_access_token("fake-token:INVALID")

    def test_BL_010_007_8_create_with_claims(self) -> None:
        token = self.provider.create_access_token("s", 60, claims={"role": "admin"})
        assert token is not None
