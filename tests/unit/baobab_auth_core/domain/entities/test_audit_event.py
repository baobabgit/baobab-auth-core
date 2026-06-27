"""Tests de l'entité AuditEvent."""

import dataclasses
from datetime import UTC, datetime

import pytest

from baobab_auth_core.domain.entities.audit_event import AuditEvent
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.value_objects.audit_event_id import AuditEventId
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestAuditEvent:
    def test_BL_010_003_1_construction_minimal(self) -> None:
        evt = AuditEvent(
            id=AuditEventId("e1"),
            event_type=AuditEventType.LOGIN_SUCCESS,
            severity=AuditSeverity.INFO,
            created_at=_NOW,
        )
        assert evt.actor_subject is None
        assert evt.target_type is None
        assert evt.metadata == {}

    def test_BL_010_003_2_construction_full(self) -> None:
        evt = AuditEvent(
            id=AuditEventId("e1"),
            event_type=AuditEventType.LOGIN_FAILURE,
            severity=AuditSeverity.WARNING,
            created_at=_NOW,
            actor_subject=AuthSubject("s1"),
            target_type="user",
            target_id="u1",
            ip_address="127.0.0.1",
            user_agent="curl/7.0",
            metadata={"reason": "bad password"},
        )
        assert evt.actor_subject == AuthSubject("s1")
        assert evt.metadata["reason"] == "bad password"

    def test_BL_010_003_3_immutable(self) -> None:
        evt = AuditEvent(
            id=AuditEventId("e1"),
            event_type=AuditEventType.LOGOUT,
            severity=AuditSeverity.INFO,
            created_at=_NOW,
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            evt.severity = AuditSeverity.CRITICAL  # type: ignore[misc]
