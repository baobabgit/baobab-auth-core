"""Port AuditRepository — persistance des événements d'audit.

:spec: BL-010-006
"""

from typing import Protocol, runtime_checkable

from baobab_auth_core.domain.entities.audit_event import AuditEvent
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject


@runtime_checkable
class AuditRepository(Protocol):
    """Protocole de persistance des entités :class:`AuditEvent`.

    Les événements d'audit sont en écriture seule (append-only) ;
    la suppression n'est pas exposée dans ce port.
    """

    def save(self, event: AuditEvent) -> None:
        """Enregistre un événement d'audit.

        :param event: Événement à persister.
        """
        ...

    def list_by_actor(self, actor_subject: AuthSubject) -> list[AuditEvent]:
        """Liste les événements d'audit d'un acteur donné.

        :param actor_subject: Sujet de l'acteur.
        :returns: Liste des événements triés par date croissante.
        """
        ...
