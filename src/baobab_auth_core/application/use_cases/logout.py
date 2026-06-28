"""Cas d'usage Logout — déconnexion idempotente d'une session.

:spec: BL-020-005
"""

from baobab_auth_core.application.commands.logout_command import LogoutCommand
from baobab_auth_core.application.services.audit_recorder import AuditRecorder
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.exceptions.authorization import ForbiddenError
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.session_repository import SessionRepository
from baobab_auth_core.ports.unit_of_work import UnitOfWork
from baobab_auth_core.ports.user_repository import UserRepository


class Logout:
    """Déconnecte (révoque) la propre session de l'utilisateur, de façon idempotente.

    Une session absente ou déjà révoquée donne un no-op silencieux.
    """

    def __init__(
        self,
        sessions: SessionRepository,
        users: UserRepository,
        audit: AuditRepository,
        id_generator: IdGenerator,
        clock: Clock,
        uow: UnitOfWork,
    ) -> None:
        """Initialise le cas d'usage avec ses dépendances injectées.

        :param sessions: Dépôt de sessions.
        :param users: Dépôt d'utilisateurs (vérification de propriété).
        :param audit: Dépôt d'audit.
        :param id_generator: Générateur d'identifiants (audit).
        :param clock: Horloge injectée.
        :param uow: Unité de travail transactionnelle.
        """
        self._sessions = sessions
        self._users = users
        self._clock = clock
        self._uow = uow
        self._recorder = AuditRecorder(audit, id_generator, clock)

    def execute(self, command: LogoutCommand) -> None:
        """Exécute la déconnexion.

        :param command: Données de déconnexion (session et acteur).
        :raises ForbiddenError: Si l'acteur n'est pas le propriétaire de la session.
        """
        session = self._sessions.get_by_id(command.session_id)
        if session is None:
            return

        actor = self._users.get_by_auth_subject(command.actor_subject)
        if actor is None or session.user_id != actor.id:
            raise ForbiddenError("L'acteur ne peut pas déconnecter cette session.")

        if session.status == SessionStatus.REVOKED:
            return

        session.revoke(self._clock.now())
        with self._uow:
            self._sessions.save(session)
            self._recorder.record(
                event_type=AuditEventType.LOGOUT,
                severity=AuditSeverity.INFO,
                actor_subject=command.actor_subject,
                target_type="session",
                target_id=str(session.id),
            )
            self._uow.commit()
