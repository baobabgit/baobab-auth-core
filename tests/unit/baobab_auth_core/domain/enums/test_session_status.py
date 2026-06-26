"""Tests de l'énumération SessionStatus."""

from baobab_auth_core.domain.enums.session_status import SessionStatus


class TestSessionStatus:
    def test_BL_010_004_1_all_values_exist(self) -> None:
        expected = {"ACTIVE", "REVOKED", "EXPIRED"}
        actual = {s.value for s in SessionStatus}
        assert actual == expected

    def test_BL_010_004_2_str_compat(self) -> None:
        assert SessionStatus.ACTIVE == "ACTIVE"
        assert SessionStatus.REVOKED == "REVOKED"
        assert SessionStatus.EXPIRED == "EXPIRED"
