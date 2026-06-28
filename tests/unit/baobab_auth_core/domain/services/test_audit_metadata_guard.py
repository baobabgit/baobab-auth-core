"""Tests du service AuditMetadataGuard.

:spec: BL-020-008
"""

import pytest

from baobab_auth_core.domain.services.audit_metadata_guard import AuditMetadataGuard
from baobab_auth_core.exceptions.validation import ValidationError


class TestAuditMetadataGuard:
    def test_BL_020_008_1_metadata_sure_passe(self) -> None:
        guard = AuditMetadataGuard()
        safe = guard.ensure_safe({"role": "ADMIN", "target_user_id": "u1"})
        assert safe == {"role": "ADMIN", "target_user_id": "u1"}

    @pytest.mark.parametrize(
        "key",
        [
            "password",
            "plain_password",
            "password_hash",
            "access_token",
            "refresh_token",
            "private_key",
            "secret",
            "authorization",
            "cookie",
            "Password",
        ],
    )
    def test_BL_020_008_2_metadata_sensible_rejetee(self, key: str) -> None:
        guard = AuditMetadataGuard()
        with pytest.raises(ValidationError):
            guard.ensure_safe({key: "x"})
