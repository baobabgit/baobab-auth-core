"""Tests de sûreté de l'audit — immutabilité et absence de secret.

:spec: BL-040-009
"""

import dataclasses
from datetime import UTC, datetime

import pytest

from baobab_auth_core.domain.entities.audit_event import AuditEvent
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.services.audit_metadata_guard import AuditMetadataGuard
from baobab_auth_core.domain.value_objects.audit_event_id import AuditEventId
from baobab_auth_core.exceptions.validation import ValidationError

_FORBIDDEN = (
    "password",
    "plain_password",
    "password_hash",
    "access_token",
    "refresh_token",
    "private_key",
    "secret",
    "cookie",
    "authorization",
)


class TestAuditEventSafety:
    def test_BL_040_009_1_audit_event_immutable(self) -> None:
        event = AuditEvent(
            id=AuditEventId("evt-1"),
            event_type=AuditEventType.PASSWORD_CHANGED,
            severity=AuditSeverity.WARNING,
            created_at=datetime(2024, 1, 1, tzinfo=UTC),
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            event.severity = AuditSeverity.INFO  # type: ignore[misc]

    @pytest.mark.parametrize("key", _FORBIDDEN)
    def test_BL_040_009_2_metadata_sensible_rejetee(self, key: str) -> None:
        guard = AuditMetadataGuard()
        with pytest.raises(ValidationError):
            guard.ensure_safe({key: "leak"})

    def test_BL_040_009_3_metadata_rbac_sure_acceptee(self) -> None:
        guard = AuditMetadataGuard()
        safe = guard.ensure_safe({"role": "ADMIN", "target_user_id": "u1", "count": 3})
        assert safe == {"role": "ADMIN", "target_user_id": "u1", "count": 3}
