"""Cas d'usage EnableUser — réactivation auditée d'un compte.

:spec: BL-050-008
"""

from baobab_auth_core.application.commands.enable_user_command import EnableUserCommand
from baobab_auth_core.application.services.audit_recorder import AuditRecorder
from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.authorization import ForbiddenError
from baobab_auth_core.exceptions.user import UserNotFoundError
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.unit_of_work import UnitOfWork
from baobab_auth_core.ports.user_repository import UserRepository

_ADMIN_ROLES = (RoleName("ADMIN"), RoleName("SUPER_ADMIN"))


class EnableUser:
    """Réactive un compte utilisateur, réservé ADMIN/SUPER_ADMIN, audité."""

    def __init__(
        self,
        users: UserRepository,
        authorization: AuthorizationService,
        audit: AuditRepository,
        id_generator: IdGenerator,
        clock: Clock,
        uow: UnitOfWork,
    ) -> None:
        """Initialise le cas d'usage avec ses dépendances injectées.

        :param users: Dépôt d'utilisateurs.
        :param authorization: Service de construction du contexte acteur.
        :param audit: Dépôt d'audit.
        :param id_generator: Générateur d'identifiants d'audit.
        :param clock: Horloge injectée.
        :param uow: Unité de travail transactionnelle.
        """
        self._users = users
        self._authorization = authorization
        self._clock = clock
        self._uow = uow
        self._recorder = AuditRecorder(audit, id_generator, clock)

    def execute(self, command: EnableUserCommand) -> None:
        """Exécute la réactivation.

        :param command: Données de réactivation.
        :raises ForbiddenError: Si l'acteur n'est pas administrateur.
        :raises UserNotFoundError: Si la cible n'existe pas.
        """
        context = self._authorization.build_context(command.actor_subject)
        if not context.has_any_role(_ADMIN_ROLES):
            raise ForbiddenError("L'acteur ne peut pas réactiver un compte.")

        target_id = (
            command.target_user_id
            if isinstance(command.target_user_id, UserId)
            else UserId(command.target_user_id)
        )
        target = self._users.get_by_id(target_id)
        if target is None:
            raise UserNotFoundError(f"Utilisateur cible introuvable : {target_id}.")

        target.activate(self._clock.now())
        with self._uow:
            self._users.save(target)
            self._recorder.record(
                event_type=AuditEventType.ACCOUNT_ENABLED,
                severity=AuditSeverity.WARNING,
                actor_subject=context.auth_subject,
                target_type="user",
                target_id=str(target.id),
                ip_address=command.ip_address,
                user_agent=command.user_agent,
            )
            self._uow.commit()
