"""Tests de l'énumération UserStatus."""

from baobab_auth_core.domain.enums.user_status import UserStatus


class TestUserStatus:
    def test_BL_010_004_1_all_values_exist(self) -> None:
        expected = {"PENDING", "ACTIVE", "LOCKED", "DISABLED", "DELETED"}
        actual = {s.value for s in UserStatus}
        assert actual == expected

    def test_BL_010_004_2_str_compat(self) -> None:
        assert UserStatus.ACTIVE == "ACTIVE"

    def test_BL_010_004_3_pending(self) -> None:
        assert UserStatus.PENDING == "PENDING"

    def test_BL_010_004_4_locked(self) -> None:
        assert UserStatus.LOCKED == "LOCKED"

    def test_BL_010_004_5_disabled(self) -> None:
        assert UserStatus.DISABLED == "DISABLED"

    def test_BL_010_004_6_deleted(self) -> None:
        assert UserStatus.DELETED == "DELETED"
