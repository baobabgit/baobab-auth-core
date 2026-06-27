"""Tests de l'énumération AuditSeverity."""

from baobab_auth_core.domain.enums.audit_severity import AuditSeverity


class TestAuditSeverity:
    def test_BL_010_004_1_all_values_exist(self) -> None:
        expected = {"INFO", "WARNING", "CRITICAL"}
        actual = {s.value for s in AuditSeverity}
        assert actual == expected

    def test_BL_010_004_2_str_compat(self) -> None:
        assert AuditSeverity.INFO == "INFO"
        assert AuditSeverity.WARNING == "WARNING"
        assert AuditSeverity.CRITICAL == "CRITICAL"
