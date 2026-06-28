"""Cas d'usage RevokeSession — révocation d'une session.

:spec: BL-020-006
"""

from baobab_auth_core.application.commands.revoke_session_command import (
    RevokeSessionCommand,
)
from baobab_auth_core.application.services.audit_recorder import AuditRecorder
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.exceptions.session import SessionNotFoundError
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.session_repository import SessionRepository
from baobab_auth_core.ports.unit_of_work import UnitOfWork


class RevokeSession:
    """Révoque une session existante et produit l'audit ``SESSION_REVOKED``.

    L'acteur est minimal en v0.2.0 (``AuthSubject``) ; les contrôles
    d'autorisation fins sont reportés à v0.3.0 (ADR-0008). Une session déjà
    révoquée donne un no-op idempotent ; une session inconnue est refusée.
    """

    def __init__(
        self,
        sessions: SessionRepository,
        audit: AuditRepository,
        id_generator: IdGenerator,
        clock: Clock,
        uow: UnitOfWork,
    ) -> None:
        """Initialise le cas d'usage avec ses dépendances injectées.

        :param sessions: Dépôt de sessions.
        :param audit: Dépôt d'audit.
        :param id_generator: Générateur d'identifiants (audit).
        :param clock: Horloge injectée.
        :param uow: Unité de travail transactionnelle.
        """
        self._sessions = sessions
        self._clock = clock
        self._uow = uow
        self._recorder = AuditRecorder(audit, id_generator, clock)

    def execute(self, command: RevokeSessionCommand) -> None:
        """Exécute la révocation.

        :param command: Données de révocation (acteur minimal et session).
        :raises SessionNotFoundError: Si la session n'existe pas.
        """
        session = self._sessions.get_by_id(command.session_id)
        if session is None:
            raise SessionNotFoundError("Session introuvable.")

        if session.status == SessionStatus.REVOKED:
            return

        session.revoke(self._clock.now())
        with self._uow:
            self._sessions.save(session)
            self._recorder.record(
                event_type=AuditEventType.SESSION_REVOKED,
                severity=AuditSeverity.WARNING,
                actor_subject=command.actor_subject,
                target_type="session",
                target_id=str(session.id),
            )
            self._uow.commit()
