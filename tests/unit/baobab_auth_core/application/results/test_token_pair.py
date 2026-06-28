"""Tests du DTO TokenPair.

:spec: BL-020-007
"""

from baobab_auth_core.application.results.token_pair import TokenPair


class TestTokenPair:
    def test_BL_020_007_1_repr_masque_les_tokens(self) -> None:
        pair = TokenPair(
            access_token="access-secret",
            refresh_token="refresh-secret",
            token_type="Bearer",
            expires_in=900,
            refresh_expires_in=2592000,
        )
        text = repr(pair)
        assert "access-secret" not in text
        assert "refresh-secret" not in text
        assert "***" in text
        assert "Bearer" in text

    def test_BL_020_007_2_valeurs_accessibles(self) -> None:
        pair = TokenPair("a", "r", "Bearer", 900, 2592000)
        assert pair.access_token == "a"
        assert pair.refresh_token == "r"
        assert pair.expires_in == 900
        assert pair.refresh_expires_in == 2592000
