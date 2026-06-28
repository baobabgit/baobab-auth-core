"""Port RoleRepository — persistance des rôles.

:spec: BL-010-006
"""

from typing import Protocol, runtime_checkable

from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName


@runtime_checkable
class RoleRepository(Protocol):
    """Protocole de persistance des entités :class:`Role`."""

    def get_by_id(self, role_id: RoleId) -> Role | None:
        """Récupère un rôle par son identifiant.

        :param role_id: Identifiant du rôle.
        :returns: Le rôle ou ``None`` s'il n'existe pas.
        """
        ...

    def get_by_name(self, name: RoleName) -> Role | None:
        """Récupère un rôle par son nom.

        :param name: Nom du rôle.
        :returns: Le rôle ou ``None`` s'il n'existe pas.
        """
        ...

    def save(self, role: Role) -> None:
        """Sauvegarde un rôle (création ou mise à jour).

        :param role: Rôle à sauvegarder.
        """
        ...

    def list_all(self) -> list[Role]:
        """Liste tous les rôles.

        :returns: Liste des rôles.
        """
        ...

    def list_roles(self) -> tuple[Role, ...]:
        """Liste tous les rôles.

        :returns: Tuple des rôles.
        """
        ...

    def count_users_with_role(self, name: RoleName) -> int:
        """Compte les utilisateurs portant un rôle.

        :param name: Nom du rôle.
        :returns: Nombre d'utilisateurs assignés à ce rôle.
        """
        ...
