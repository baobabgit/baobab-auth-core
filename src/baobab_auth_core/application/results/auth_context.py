"""DTO AuthContext — contexte d'autorisation métier.

:spec: BL-030-001
"""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.user_id import UserId


def _deduplicate_roles(values: tuple[RoleName, ...]) -> tuple[RoleName, ...]:
    """Déduplique les rôles en conservant leur ordre.

    :param values: Valeurs à dédupliquer.
    :returns: Tuple sans doublon.
    """
    seen: set[RoleName] = set()
    deduplicated: list[RoleName] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            deduplicated.append(value)
    return tuple(deduplicated)


def _deduplicate_permissions(
    values: tuple[PermissionName, ...],
) -> tuple[PermissionName, ...]:
    """Déduplique les permissions en conservant leur ordre.

    :param values: Valeurs à dédupliquer.
    :returns: Tuple sans doublon.
    """
    seen: set[PermissionName] = set()
    deduplicated: list[PermissionName] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            deduplicated.append(value)
    return tuple(deduplicated)


@dataclass(frozen=True)
class AuthContext:
    """Contexte immutable utilisé par les décisions d'autorisation.

    Le contexte ne contient aucun secret. Il agrège uniquement le sujet
    d'authentification, les identifiants métier, les rôles et les permissions.

    :param auth_subject: Sujet d'authentification stable.
    :param user_id: Identifiant utilisateur, ou ``None`` pour un sujet non utilisateur.
    :param session_id: Identifiant de session courant, ou ``None``.
    :param roles: Rôles disponibles dans le contexte.
    :param permissions: Permissions disponibles dans le contexte.
    :param authenticated_at: Date d'authentification, ou ``None``.
    """

    auth_subject: AuthSubject
    user_id: UserId | str | None
    session_id: SessionId | None
    roles: tuple[RoleName, ...]
    permissions: tuple[PermissionName, ...]
    authenticated_at: datetime | None

    def __post_init__(self) -> None:
        """Déduplique les rôles et permissions.

        :returns: ``None``.
        """
        object.__setattr__(self, "roles", _deduplicate_roles(self.roles))
        object.__setattr__(
            self,
            "permissions",
            _deduplicate_permissions(self.permissions),
        )

    def has_role(self, role: RoleName | str) -> bool:
        """Indique si le contexte contient un rôle.

        :param role: Rôle à vérifier.
        :returns: ``True`` si le rôle est présent.
        """
        return self._coerce_role(role) in self.roles

    def has_any_role(self, roles: Iterable[RoleName | str]) -> bool:
        """Indique si au moins un rôle est présent.

        :param roles: Rôles à vérifier.
        :returns: ``True`` si au moins un rôle est présent.
        """
        return any(self.has_role(role) for role in roles)

    def has_permission(self, permission: PermissionName | str) -> bool:
        """Indique si le contexte contient une permission.

        :param permission: Permission à vérifier.
        :returns: ``True`` si la permission est présente.
        """
        return self._coerce_permission(permission) in self.permissions

    def has_any_permission(self, permissions: Iterable[PermissionName | str]) -> bool:
        """Indique si au moins une permission est présente.

        :param permissions: Permissions à vérifier.
        :returns: ``True`` si au moins une permission est présente.
        """
        return any(self.has_permission(permission) for permission in permissions)

    def has_all_permissions(self, permissions: Iterable[PermissionName | str]) -> bool:
        """Indique si toutes les permissions sont présentes.

        :param permissions: Permissions à vérifier.
        :returns: ``True`` si toutes les permissions sont présentes.
        """
        return all(self.has_permission(permission) for permission in permissions)

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
        :returns: Permission validée.
        """
        if isinstance(permission, PermissionName):
            return permission
        return PermissionName(permission)
