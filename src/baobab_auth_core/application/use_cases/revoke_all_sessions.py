"""Cas d'usage RevokeAllSessions — révocation de masse des sessions d'un compte.

:spec: BL-040-014
"""

from baobab_auth_core.application.commands.revoke_all_sessions_command import (
    RevokeAllSessionsCommand,
)
from baobab_auth_core.application.results.auth_context import AuthContext
from baobab_auth_core.application.services.audit_recorder import AuditRecorder
from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.policies.role_policy import RolePolicy
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.authorization import ForbiddenError
from baobab_auth_core.exceptions.user import UserNotFoundError
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.session_repository import SessionRepository
from baobab_auth_core.ports.unit_of_work import UnitOfWork
from baobab_auth_core.ports.user_repository import UserRepository

_ADMIN_ROLE = RoleName("ADMIN")


class RevokeAllSessions:
    """Révoque toutes les sessions actives d'un utilisateur cible.

    Un utilisateur révoque ses propres sessions ; un ``ADMIN`` (ou ``SUPER_ADMIN``)
    révoque celles d'un compte standard. Un ``SUPER_ADMIN`` ne peut être neutralisé
    que par un autre ``SUPER_ADMIN``. Audit ``ALL_SESSIONS_REVOKED`` avec ``count``.
    """

    def __init__(
        self,
        authorization: AuthorizationService,
        users: UserRepository,
        sessions: SessionRepository,
        audit: AuditRepository,
        id_generator: IdGenerator,
        clock: Clock,
        uow: UnitOfWork,
        role_policy: RolePolicy | None = None,
    ) -> None:
        """Initialise le cas d'usage avec ses dépendances injectées.

        :param authorization: Service de construction du contexte acteur.
        :param users: Dépôt d'utilisateurs.
        :param sessions: Dépôt de sessions.
        :param audit: Dépôt d'audit.
        :param id_generator: Générateur d'identifiants d'audit.
        :param clock: Horloge injectée.
        :param uow: Unité de travail transactionnelle.
        :param role_policy: Politique de rôle (rôle super-admin).
        """
        self._authorization = authorization
        self._users = users
        self._sessions = sessions
        self._clock = clock
        self._uow = uow
        self._policy = role_policy or RolePolicy()
        self._recorder = AuditRecorder(audit, id_generator, clock)

    def execute(self, command: RevokeAllSessionsCommand) -> int:
        """Exécute la révocation de masse.

        :param command: Données de révocation.
        :returns: Nombre de sessions révoquées.
        :raises UserNotFoundError: Si la cible n'existe pas.
        :raises ForbiddenError: Si l'acteur n'est pas autorisé.
        """
        actor_context = self._authorization.build_context(command.actor_subject)
        target = self._get_target(command.target_user_id)
        self._authorize(actor_context, target)

        now = self._clock.now()
        revoked = list(self._sessions.get_active_by_user(target.id))
        for session in revoked:
            session.revoke(now)

        with self._uow:
            for session in revoked:
                self._sessions.save(session)
            self._recorder.record(
                event_type=AuditEventType.ALL_SESSIONS_REVOKED,
                severity=AuditSeverity.WARNING,
                actor_subject=actor_context.auth_subject,
                target_type="user",
                target_id=str(target.id),
                ip_address=command.ip_address,
                user_agent=command.user_agent,
                metadata={"count": len(revoked)},
            )
            self._uow.commit()
        return len(revoked)

    def _authorize(self, actor_context: AuthContext, target: User) -> None:
        """Vérifie que l'acteur peut révoquer les sessions de la cible.

        :param actor_context: Contexte de l'acteur.
        :param target: Utilisateur cible.
        :raises ForbiddenError: Si l'acteur n'est pas autorisé.
        """
        if actor_context.user_id == target.id:
            return
        allowed_roles = (_ADMIN_ROLE, self._policy.super_admin_role_name)
        if not actor_context.has_any_role(allowed_roles):
            raise ForbiddenError("L'acteur ne peut pas révoquer ces sessions.")
        target_is_super_admin = target.has_role(self._policy.super_admin_role_name)
        if target_is_super_admin and not actor_context.has_role(
            self._policy.super_admin_role_name
        ):
            raise ForbiddenError(
                "Seul un SUPER_ADMIN peut révoquer les sessions d'un SUPER_ADMIN."
            )

    def _get_target(self, target_user_id: UserId | str) -> User:
        """Charge l'utilisateur cible.

        :param target_user_id: Identifiant cible.
        :returns: Utilisateur cible.
        :raises UserNotFoundError: Si la cible n'existe pas.
        """
        user_id = (
            target_user_id
            if isinstance(target_user_id, UserId)
            else UserId(target_user_id)
        )
        target = self._users.get_by_id(user_id)
        if target is None:
            raise UserNotFoundError(f"Utilisateur cible introuvable : {user_id}.")
        return target
