"""Tests de l'énumération AuditEventType."""

from baobab_auth_core.domain.enums.audit_event_type import AuditEventType


class TestAuditEventType:
    def test_BL_010_004_1_all_values_exist(self) -> None:
        expected = {
            "USER_REGISTERED",
            "LOGIN_SUCCESS",
            "LOGIN_FAILURE",
            "LOGOUT",
            "SESSION_REFRESHED",
            "SESSION_REVOKED",
            "ROLE_ASSIGNED",
            "ROLE_REMOVED",
            "PASSWORD_CHANGED",
            "ACCOUNT_LOCKED",
            "ACCOUNT_DISABLED",
            "ACCOUNT_DELETED",
        }
        actual = {e.value for e in AuditEventType}
        assert actual == expected

    def test_BL_010_004_2_str_compat(self) -> None:
        assert AuditEventType.LOGIN_SUCCESS == "LOGIN_SUCCESS"
        assert AuditEventType.LOGIN_FAILURE == "LOGIN_FAILURE"

    def test_BL_010_004_3_count(self) -> None:
        assert len(AuditEventType) == 12
