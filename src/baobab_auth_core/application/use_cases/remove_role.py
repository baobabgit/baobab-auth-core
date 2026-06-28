"""Cas d'usage RemoveRole — retrait RBAC audité.

:spec: BL-030-005
"""

from baobab_auth_core.application.commands.remove_role_command import (
    RemoveRoleCommand,
)
from baobab_auth_core.application.results.auth_context import AuthContext
from baobab_auth_core.application.services.audit_recorder import AuditRecorder
from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.policies.role_policy import RolePolicy
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.authorization import ForbiddenError
from baobab_auth_core.exceptions.role import (
    LastSuperAdminRoleRemovalError,
    RoleNotFoundError,
)
from baobab_auth_core.exceptions.user import UserNotFoundError
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.role_repository import RoleRepository
from baobab_auth_core.ports.unit_of_work import UnitOfWork
from baobab_auth_core.ports.user_repository import UserRepository

_ALLOWED_ACTOR_ROLES = (RoleName("ADMIN"), RoleName("SUPER_ADMIN"))


class RemoveRole:
    """Retire un rôle existant d'un utilisateur cible.

    L'acteur doit porter ``ADMIN`` ou ``SUPER_ADMIN`` en v0.3.0. Une cible qui
    ne possède pas le rôle produit un no-op idempotent.

    :param users: Dépôt d'utilisateurs.
    :param roles: Dépôt de rôles.
    :param authorization: Service de construction du contexte acteur.
    :param audit: Dépôt d'audit.
    :param id_generator: Générateur d'identifiants d'audit.
    :param clock: Horloge injectée.
    :param uow: Unité de travail transactionnelle.
    :param role_policy: Politique de retrait des rôles.
    :spec: BL-030-005
    """

    def __init__(
        self,
        users: UserRepository,
        roles: RoleRepository,
        authorization: AuthorizationService,
        audit: AuditRepository,
        id_generator: IdGenerator,
        clock: Clock,
        uow: UnitOfWork,
        role_policy: RolePolicy | None = None,
    ) -> None:
        """Initialise le cas d'usage avec ses dépendances injectées.

        :param users: Dépôt d'utilisateurs.
        :param roles: Dépôt de rôles.
        :param authorization: Service de construction du contexte acteur.
        :param audit: Dépôt d'audit.
        :param id_generator: Générateur d'identifiants d'audit.
        :param clock: Horloge injectée.
        :param uow: Unité de travail transactionnelle.
        :param role_policy: Politique de retrait des rôles.
        :spec: BL-030-005
        """
        self._users = users
        self._roles = roles
        self._authorization = authorization
        self._clock = clock
        self._uow = uow
        self._policy = role_policy or RolePolicy()
        self._recorder = AuditRecorder(audit, id_generator, clock)

    def execute(self, command: RemoveRoleCommand) -> None:
        """Exécute le retrait de rôle.

        :param command: Données de retrait.
        :raises UserNotFoundError: Si l'acteur ou la cible n'existe pas.
        :raises ForbiddenError: Si l'acteur n'est pas autorisé.
        :raises RoleNotFoundError: Si le rôle demandé n'existe pas.
        :raises LastSuperAdminRoleRemovalError: Si le dernier super-admin est retiré.
        :spec: BL-030-005
        """
        actor_context = self._authorization.build_context(command.actor_subject)
        self._require_allowed_actor(actor_context)

        target = self._get_target_user(command.target_user_id)
        role = self._get_role(command.role_name)
        if not target.has_role(role.name):
            return

        self._ensure_removable(role)
        target.remove_role(role.name, self._clock.now())
        with self._uow:
            self._users.save(target)
            self._recorder.record(
                event_type=AuditEventType.ROLE_REMOVED,
                severity=AuditSeverity.WARNING,
                actor_subject=actor_context.auth_subject,
                target_type="user",
                target_id=str(target.id),
                ip_address=command.ip_address,
                user_agent=command.user_agent,
                metadata={
                    "role": str(role.name),
                    "target_user_id": str(target.id),
                },
            )
            self._uow.commit()

    def _require_allowed_actor(self, actor_context: AuthContext) -> None:
        """Vérifie que l'acteur possède un rôle autorisé.

        :param actor_context: Contexte d'autorisation de l'acteur.
        :raises ForbiddenError: Si l'acteur n'est pas autorisé.
        """
        if not actor_context.has_any_role(_ALLOWED_ACTOR_ROLES):
            raise ForbiddenError("L'acteur ne peut pas retirer de rôle.")

    def _get_target_user(self, target_user_id: UserId | str) -> User:
        """Charge l'utilisateur cible.

        :param target_user_id: Identifiant cible.
        :returns: Utilisateur cible.
        :raises UserNotFoundError: Si la cible n'existe pas.
        """
        user_id = self._coerce_user_id(target_user_id)
        target = self._users.get_by_id(user_id)
        if target is None:
            raise UserNotFoundError(f"Utilisateur cible introuvable : {user_id}.")
        return target

    def _get_role(self, role_name: RoleName | str) -> Role:
        """Charge le rôle demandé.

        :param role_name: Nom du rôle.
        :returns: Rôle connu.
        :raises RoleNotFoundError: Si le rôle n'existe pas.
        """
        requested_role = self._coerce_role_name(role_name)
        role = self._roles.get_by_name(requested_role)
        if role is None:
            raise RoleNotFoundError(f"Rôle introuvable : {requested_role}.")
        return role

    def _ensure_removable(self, role: Role) -> None:
        """Vérifie que le retrait respecte la politique de rôle.

        :param role: Rôle à retirer.
        :raises LastSuperAdminRoleRemovalError: Si le dernier super-admin est retiré.
        """
        users_with_role = self._roles.count_users_with_role(role.name)
        if not self._policy.can_remove_role(role.name, users_with_role):
            raise LastSuperAdminRoleRemovalError(
                "Impossible de retirer le dernier SUPER_ADMIN."
            )

    @staticmethod
    def _coerce_user_id(user_id: UserId | str) -> UserId:
        """Convertit un identifiant texte en :class:`UserId`.

        :param user_id: Identifiant à convertir.
        :returns: Identifiant utilisateur.
        """
        if isinstance(user_id, UserId):
            return user_id
        return UserId(user_id)

    @staticmethod
    def _coerce_role_name(role_name: RoleName | str) -> RoleName:
        """Convertit un rôle texte en :class:`RoleName`.

        :param role_name: Rôle à convertir.
        :returns: Rôle normalisé.
        """
        if isinstance(role_name, RoleName):
            return role_name
        return RoleName(role_name)
