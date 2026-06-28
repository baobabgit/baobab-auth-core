"""Service AuditRecorder — construit et persiste les événements d'audit.

:spec: BL-020-008
"""

from collections.abc import Mapping
from typing import Any

from baobab_auth_core.domain.entities.audit_event import AuditEvent
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.services.audit_metadata_guard import AuditMetadataGuard
from baobab_auth_core.domain.value_objects.audit_event_id import AuditEventId
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator


class AuditRecorder:
    """Construit des :class:`AuditEvent` sûrs et les persiste via le port d'audit.

    Centralise la création des événements d'audit et garantit, via
    :class:`AuditMetadataGuard`, qu'aucun secret n'est journalisé.
    """

    def __init__(
        self,
        audit_repository: AuditRepository,
        id_generator: IdGenerator,
        clock: Clock,
        guard: AuditMetadataGuard | None = None,
    ) -> None:
        """Initialise le recorder.

        :param audit_repository: Port de persistance des événements d'audit.
        :param id_generator: Générateur d'identifiants.
        :param clock: Horloge injectée.
        :param guard: Garde anti-fuite (défaut : :class:`AuditMetadataGuard`).
        """
        self._audit = audit_repository
        self._ids = id_generator
        self._clock = clock
        self._guard = guard or AuditMetadataGuard()

    def record(
        self,
        event_type: AuditEventType,
        severity: AuditSeverity,
        actor_subject: AuthSubject | None = None,
        target_type: str | None = None,
        target_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> AuditEvent:
        """Construit, valide et persiste un événement d'audit.

        :param event_type: Type d'événement.
        :param severity: Sévérité.
        :param actor_subject: Acteur initiateur (ou None).
        :param target_type: Type de ressource ciblée.
        :param target_id: Identifiant de la ressource ciblée.
        :param ip_address: Adresse IP de l'acteur.
        :param user_agent: User-Agent de l'acteur.
        :param metadata: Métadonnées additionnelles (sans secret).
        :returns: L'événement d'audit persisté.
        :raises ValidationError: Si les métadonnées contiennent une clé sensible.
        """
        safe_metadata = self._guard.ensure_safe(metadata or {})
        event = AuditEvent(
            id=AuditEventId(self._ids.generate()),
            event_type=event_type,
            severity=severity,
            created_at=self._clock.now(),
            actor_subject=actor_subject,
            target_type=target_type,
            target_id=target_id,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=safe_metadata,
        )
        self._audit.save(event)
        return event
