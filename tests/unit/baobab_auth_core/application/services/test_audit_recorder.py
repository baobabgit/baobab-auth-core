"""Tests du service AuditRecorder.

:spec: BL-020-008
"""

import pytest

from baobab_auth_core.application.services.audit_recorder import AuditRecorder
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.exceptions.validation import ValidationError
from baobab_auth_core.testing.fake_clock import FakeClock
from baobab_auth_core.testing.fake_id_generator import FakeIdGenerator
from baobab_auth_core.testing.in_memory_audit_repository import InMemoryAuditRepository


class TestAuditRecorder:
    def _recorder(self) -> tuple[AuditRecorder, InMemoryAuditRepository]:
        audit = InMemoryAuditRepository()
        recorder = AuditRecorder(audit, FakeIdGenerator(), FakeClock())
        return recorder, audit

    def test_BL_020_008_1_record_persiste_l_evenement(self) -> None:
        recorder, audit = self._recorder()
        event = recorder.record(
            event_type=AuditEventType.LOGIN_SUCCESS,
            severity=AuditSeverity.INFO,
            actor_subject=AuthSubject("subj-1"),
            metadata={"reason": "ok"},
        )
        assert event in audit.all_events
        assert event.event_type == AuditEventType.LOGIN_SUCCESS
        assert event.metadata == {"reason": "ok"}

    def test_BL_020_008_2_metadata_sensible_rejetee(self) -> None:
        recorder, audit = self._recorder()
        with pytest.raises(ValidationError):
            recorder.record(
                event_type=AuditEventType.LOGIN_SUCCESS,
                severity=AuditSeverity.INFO,
                metadata={"access_token": "leak"},
            )
        assert audit.all_events == []
