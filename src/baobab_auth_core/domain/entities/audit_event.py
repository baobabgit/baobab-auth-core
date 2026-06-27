"""Entité AuditEvent — événement d'audit immuable.

:spec: BL-010-003
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.value_objects.audit_event_id import AuditEventId
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject


@dataclass(frozen=True)
class AuditEvent:
    """Événement d'audit immuable tracé dans le journal de sécurité.

    Cette entité est frozen (immuable) car les événements d'audit
    ne doivent jamais être modifiés après enregistrement.

    :param id: Identifiant unique de l'événement.
    :param event_type: Type de l'événement.
    :param severity: Niveau de sévérité.
    :param created_at: Horodatage de l'événement (UTC).
    :param actor_subject: Sujet initiateur de l'action
        (ou None pour des actions système).
    :param target_type: Type de la ressource ciblée (ex. ``user``, ``session``).
    :param target_id: Identifiant de la ressource ciblée.
    :param ip_address: Adresse IP de l'acteur.
    :param user_agent: User-Agent HTTP de l'acteur.
    :param metadata: Métadonnées additionnelles contextuelles.
    """

    id: AuditEventId
    event_type: AuditEventType
    severity: AuditSeverity
    created_at: datetime
    actor_subject: AuthSubject | None = field(default=None)
    target_type: str | None = field(default=None)
    target_id: str | None = field(default=None)
    ip_address: str | None = field(default=None)
    user_agent: str | None = field(default=None)
    metadata: Mapping[str, Any] = field(default_factory=dict)
