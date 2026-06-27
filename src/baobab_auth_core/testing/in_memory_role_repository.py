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
        return list(self._store.values())

    def clear(self) -> None:
        """Vide le dépôt."""
        self._store.clear()
