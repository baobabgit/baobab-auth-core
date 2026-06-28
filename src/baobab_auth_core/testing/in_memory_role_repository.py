"""Fake InMemoryRoleRepository — dépôt de rôles en mémoire pour les tests.

:spec: BL-010-007
"""

from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName


class InMemoryRoleRepository:
    """Dépôt de rôles en mémoire pour les tests unitaires."""

    def __init__(self) -> None:
        """Initialise le dépôt avec un stockage vide."""
        self._store: dict[str, Role] = {}
        self._user_counts: dict[str, int] = {}

    def get_by_id(self, role_id: RoleId) -> Role | None:
        """Récupère un rôle par son identifiant.

        :param role_id: Identifiant du rôle.
        :returns: Le rôle ou ``None``.
        """
        return self._store.get(role_id.value)

    def get_by_name(self, name: RoleName) -> Role | None:
        """Récupère un rôle par son nom.

        :param name: Nom du rôle.
        :returns: Le rôle ou ``None``.
        """
        for role in self._store.values():
            if role.name == name:
                return role
        return None

    def save(self, role: Role) -> None:
        """Sauvegarde un rôle.

        :param role: Rôle à sauvegarder.
        """
        self._store[role.id.value] = role

    def list_all(self) -> list[Role]:
        """Liste tous les rôles.

        :returns: Liste des rôles.
        """
        return list(self.list_roles())

    def list_roles(self) -> tuple[Role, ...]:
        """Liste tous les rôles.

        :returns: Tuple des rôles.
        """
        return tuple(self._store.values())

    def count_users_with_role(self, name: RoleName) -> int:
        """Compte les utilisateurs portant un rôle.

        :param name: Nom du rôle.
        :returns: Nombre d'utilisateurs portant ce rôle.
        """
        return self._user_counts.get(name.value, 0)

    def set_users_with_role_count(self, name: RoleName, count: int) -> None:
        """Configure le nombre d'utilisateurs portant un rôle.

        :param name: Nom du rôle.
        :param count: Nombre d'utilisateurs à exposer.
        :raises ValueError: Si ``count`` est négatif.
        """
        if count < 0:
            raise ValueError("count doit être supérieur ou égal à zéro.")
        self._user_counts[name.value] = count

    def clear(self) -> None:
        """Vide le dépôt."""
        self._store.clear()
        self._user_counts.clear()
