"""Service AuthorizationService — décisions d'autorisation RBAC.

:spec: BL-030-002
"""

from baobab_auth_core.application.results.auth_context import AuthContext
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.exceptions.authorization import (
    ForbiddenError,
    PermissionDeniedError,
)
from baobab_auth_core.exceptions.user import UserNotFoundError
from baobab_auth_core.ports.permission_repository import PermissionRepository
from baobab_auth_core.ports.role_repository import RoleRepository
from baobab_auth_core.ports.user_repository import UserRepository


class AuthorizationService:
    """Service applicatif de construction et de vérification RBAC.

    :param user_repository: Port de lecture des utilisateurs.
    :param role_repository: Port de lecture des rôles.
    :param permission_repository: Port de lecture des permissions.
    :spec: BL-030-002
    """

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
    ) -> None:
        """Initialise le service d'autorisation.

        :param user_repository: Port de lecture des utilisateurs.
        :param role_repository: Port de lecture des rôles.
        :param permission_repository: Port de lecture des permissions.
        :spec: BL-030-002
        """
        self._users = user_repository
        self._roles = role_repository
        self._permissions = permission_repository

    def build_context(self, auth_subject: AuthSubject | str) -> AuthContext:
        """Construit le contexte RBAC d'un sujet authentifié.

        Les rôles inconnus sont ignorés en v0.3.0 conformément à l'ADR-0009.

        :param auth_subject: Sujet d'authentification stable.
        :returns: Contexte d'autorisation prêt à vérifier.
        :raises UserNotFoundError: Si aucun utilisateur ne correspond au sujet.
        :spec: BL-030-002
        """
        subject = self._coerce_auth_subject(auth_subject)
        user = self._users.get_by_auth_subject(subject)
        if user is None:
            raise UserNotFoundError(
                f"Utilisateur introuvable pour le sujet '{subject}'."
            )

        roles = self._load_known_roles(user.role_names)
        permissions = self._load_known_permissions(roles)
        return AuthContext(
            auth_subject=user.auth_subject,
            user_id=user.id,
            session_id=None,
            roles=tuple(role.name for role in roles),
            permissions=permissions,
            authenticated_at=user.last_login_at,
        )

    def has_role(self, context: AuthContext, role: RoleName | str) -> bool:
        """Vérifie si un contexte possède un rôle.

        :param context: Contexte d'autorisation.
        :param role: Rôle à vérifier.
        :returns: ``True`` si le rôle est présent.
        :spec: BL-030-002
        """
        return context.has_role(role)

    def has_permission(
        self,
        context: AuthContext,
        permission: PermissionName | str,
    ) -> bool:
        """Vérifie si un contexte possède une permission.

        :param context: Contexte d'autorisation.
        :param permission: Permission à vérifier.
        :returns: ``True`` si la permission est présente.
        :spec: BL-030-002
        """
        return context.has_permission(permission)

    def require_role(self, context: AuthContext, role: RoleName | str) -> None:
        """Exige la présence d'un rôle dans le contexte.

        :param context: Contexte d'autorisation.
        :param role: Rôle requis.
        :raises ForbiddenError: Si le rôle requis est absent.
        :spec: BL-030-002
        """
        role_name = self._coerce_role(role)
        if not context.has_role(role_name):
            raise ForbiddenError(f"Rôle requis absent : {role_name}.")

    def require_permission(
        self,
        context: AuthContext,
        permission: PermissionName | str,
    ) -> None:
        """Exige la présence d'une permission dans le contexte.

        :param context: Contexte d'autorisation.
        :param permission: Permission requise.
        :raises PermissionDeniedError: Si la permission requise est absente.
        :spec: BL-030-002
        """
        permission_name = self._coerce_permission(permission)
        if not context.has_permission(permission_name):
            raise PermissionDeniedError(
                f"Permission requise absente : {permission_name}."
            )

    @staticmethod
    def _coerce_auth_subject(auth_subject: AuthSubject | str) -> AuthSubject:
        """Convertit un sujet texte en :class:`AuthSubject`.

        :param auth_subject: Sujet à convertir.
        :returns: Sujet d'authentification.
        """
        if isinstance(auth_subject, AuthSubject):
            return auth_subject
        return AuthSubject(auth_subject)

    @staticmethod
    def _coerce_role(role: RoleName | str) -> RoleName:
        """Convertit un rôle texte en :class:`RoleName`.

        :param role: Rôle à convertir.
        :returns: Rôle normalisé.
        """
        if isinstance(role, RoleName):
            return role
        return RoleName(role)

    @staticmethod
    def _coerce_permission(permission: PermissionName | str) -> PermissionName:
        """Convertit une permission texte en :class:`PermissionName`.

        :param permission: Permission à convertir.
        :returns: Permission normalisée.
        """
        if isinstance(permission, PermissionName):
            return permission
        return PermissionName(permission)

    def _load_known_roles(self, role_names: tuple[RoleName, ...]) -> tuple[Role, ...]:
        """Charge les rôles existants en ignorant les références inconnues.

        :param role_names: Noms de rôles associés à l'utilisateur.
        :returns: Rôles connus.
        """
        roles: list[Role] = []
        for role_name in role_names:
            role = self._roles.get_by_name(role_name)
            if role is not None:
                roles.append(role)
        return tuple(roles)

    def _load_known_permissions(
        self,
        roles: tuple[Role, ...],
    ) -> tuple[PermissionName, ...]:
        """Charge les permissions existantes portées par les rôles connus.

        :param roles: Rôles connus à analyser.
        :returns: Permissions connues.
        """
        permission_names: list[PermissionName] = []
        for role in roles:
            for permission_name in role.permission_names:
                permission = self._permissions.get_by_name(permission_name)
                if permission is not None:
                    permission_names.append(permission.name)
        return tuple(permission_names)
