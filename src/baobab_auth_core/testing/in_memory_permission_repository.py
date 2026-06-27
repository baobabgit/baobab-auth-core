"""Fake InMemoryPermissionRepository — dépôt de permissions en mémoire pour les tests.

:spec: BL-010-007
"""

from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName


class InMemoryPermissionRepository:
    """Dépôt de permissions en mémoire pour les tests unitaires."""

    def __init__(self) -> None:
        """Initialise le dépôt avec un stockage vide."""
        self._store: dict[str, Permission] = {}

    def get_by_id(self, permission_id: PermissionId) -> Permission | None:
        """Récupère une permission par son identifiant.

        :param permission_id: Identifiant de la permission.
        :returns: La permission ou ``None``.
        """
        return self._store.get(permission_id.value)

    def get_by_name(self, name: PermissionName) -> Permission | None:
        """Récupère une permission par son nom.

        :param name: Nom de la permission.
        :returns: La permission ou ``None``.
        """
        for perm in self._store.values():
            if perm.name == name:
                return perm
        return None

    def save(self, permission: Permission) -> None:
        """Sauvegarde une permission.

        :param permission: Permission à sauvegarder.
        """
        self._store[permission.id.value] = permission

    def list_all(self) -> list[Permission]:
        """Liste toutes les permissions.

        :returns: Liste des permissions.
        """
        return list(self._store.values())

    def clear(self) -> None:
        """Vide le dépôt."""
        self._store.clear()
