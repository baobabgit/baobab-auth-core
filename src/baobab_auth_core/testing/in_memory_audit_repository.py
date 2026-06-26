"""Fake InMemoryAuditRepository — dépôt d'audit en mémoire pour les tests.

:spec: BL-010-007
"""

from baobab_auth_core.domain.entities.audit_event import AuditEvent
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject


class InMemoryAuditRepository:
    """Dépôt d'événements d'audit en mémoire pour les tests unitaires."""

    def __init__(self) -> None:
        """Initialise le dépôt avec une liste vide."""
        self._events: list[AuditEvent] = []

    def save(self, event: AuditEvent) -> None:
        """Enregistre un événement d'audit.

        :param event: Événement à persister.
        """
        self._events.append(event)

    def list_by_actor(self, actor_subject: AuthSubject) -> list[AuditEvent]:
        """Liste les événements d'un acteur donné.

        :param actor_subject: Sujet de l'acteur.
        :returns: Liste des événements de l'acteur.
        """
        return [e for e in self._events if e.actor_subject == actor_subject]

    @property
    def all_events(self) -> list[AuditEvent]:
        """Retourne tous les événements enregistrés.

        :returns: Copie de la liste des événements.
        """
        return list(self._events)

    def clear(self) -> None:
        """Vide le dépôt."""
        self._events.clear()
