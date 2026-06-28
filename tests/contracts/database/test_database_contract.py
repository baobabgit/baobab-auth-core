"""Contrat ``database`` — ports de persistance et seed catalogue.

Ce test n'importe **que** ``baobab_auth_core`` (aucune autre brique).

:spec: BL-050-009
"""

import json
from datetime import UTC, datetime

import baobab_auth_core as core
from baobab_auth_core import (
    AuditEvent,
    AuditEventId,
    AuditEventType,
    AuditSeverity,
    DefaultAuthCatalog,
)


class TestDatabaseContract:
    def test_BL_050_009_1_ports_persistance_exposes(self) -> None:
        for name in (
            "UserRepository",
            "RoleRepository",
            "PermissionRepository",
            "SessionRepository",
            "AuditRepository",
            "UnitOfWork",
        ):
            assert hasattr(core, name)

    def test_BL_050_009_2_catalogue_pour_seed(self) -> None:
        catalog = DefaultAuthCatalog()
        assert catalog.roles()
        assert catalog.permissions()
        assert catalog.role_permissions()

    def test_BL_050_009_3_audit_metadata_json_serialisable(self) -> None:
        event = AuditEvent(
            id=AuditEventId("e1"),
            event_type=AuditEventType.LOGIN_SUCCESS,
            severity=AuditSeverity.INFO,
            created_at=datetime(2024, 1, 1, tzinfo=UTC),
            metadata={"role": "ADMIN", "count": 3},
        )
        assert json.dumps(dict(event.metadata)) == '{"role": "ADMIN", "count": 3}'
