"""Cas d'usage BootstrapSuperAdmin — amorçage du premier super-administrateur.

:spec: BL-050-008
"""

from baobab_auth_core.application.commands.bootstrap_super_admin_command import (
    BootstrapSuperAdminCommand,
)
from baobab_auth_core.application.services.audit_recorder import AuditRecorder
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.policies.role_policy import RolePolicy
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.authorization import ForbiddenError
from baobab_auth_core.exceptions.user import UserNotFoundError
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.role_repository import RoleRepository
from baobab_auth_core.ports.unit_of_work import UnitOfWork
from baobab_auth_core.ports.user_repository import UserRepository


class BootstrapSuperAdmin:
    """Promeut un utilisateur ``SUPER_ADMIN`` lors de l'amorçage du système.

    N'opère que s'il n'existe **aucun** ``SUPER_ADMIN`` : permet de créer le
    premier super-admin sans acteur super-admin préexistant. Idempotence : si la
    cible est déjà ``SUPER_ADMIN`` et seule, no-op. Audit ``ROLE_ASSIGNED``.
    """

    def __init__(
        self,
        users: UserRepository,
        roles: RoleRepository,
        audit: AuditRepository,
        id_generator: IdGenerator,
        clock: Clock,
        uow: UnitOfWork,
        role_policy: RolePolicy | None = None,
    ) -> None:
        """Initialise le cas d'usage avec ses dépendances injectées.

        :param users: Dépôt d'utilisateurs.
        :param roles: Dépôt de rôles (compte des super-admins).
        :param audit: Dépôt d'audit.
        :param id_generator: Générateur d'identifiants d'audit.
        :param clock: Horloge injectée.
        :param uow: Unité de travail transactionnelle.
        :param role_policy: Politique de rôle (nom du rôle super-admin).
        """
        self._users = users
        self._roles = roles
        self._clock = clock
        self._uow = uow
        self._policy = role_policy or RolePolicy()
        self._recorder = AuditRecorder(audit, id_generator, clock)

    def execute(self, command: BootstrapSuperAdminCommand) -> None:
        """Exécute l'amorçage.

        :param command: Données d'amorçage.
        :raises ForbiddenError: Si un ``SUPER_ADMIN`` existe déjà.
        :raises UserNotFoundError: Si la cible n'existe pas.
        """
        super_admin = self._policy.super_admin_role_name
        if self._roles.count_users_with_role(super_admin) > 0:
            raise ForbiddenError("Un SUPER_ADMIN existe déjà : amorçage interdit.")

        target_id = (
            command.target_user_id
            if isinstance(command.target_user_id, UserId)
            else UserId(command.target_user_id)
        )
        target = self._users.get_by_id(target_id)
        if target is None:
            raise UserNotFoundError(f"Utilisateur cible introuvable : {target_id}.")

        now = self._clock.now()
        target.assign_role(super_admin, now)
        actor = self._coerce_actor(command.actor_subject) or target.auth_subject
        with self._uow:
            self._users.save(target)
            self._recorder.record(
                event_type=AuditEventType.ROLE_ASSIGNED,
                severity=AuditSeverity.WARNING,
                actor_subject=actor,
                target_type="user",
                target_id=str(target.id),
                ip_address=command.ip_address,
                user_agent=command.user_agent,
                metadata={"role": str(super_admin), "target_user_id": str(target.id)},
            )
            self._uow.commit()

    @staticmethod
    def _coerce_actor(actor: AuthSubject | str | None) -> AuthSubject | None:
        """Convertit l'acteur optionnel en :class:`AuthSubject`.

        :param actor: Acteur fourni (ou None).
        :returns: ``AuthSubject`` ou None.
        """
        if actor is None or isinstance(actor, AuthSubject):
            return actor
        return AuthSubject(actor)
