"""Port PermissionRepository — persistance des permissions.

:spec: BL-010-006
"""

from typing import Protocol, runtime_checkable

from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName


@runtime_checkable
class PermissionRepository(Protocol):
    """Protocole de persistance des entités :class:`Permission`."""

    def get_by_id(self, permission_id: PermissionId) -> Permission | None:
        """Récupère une permission par son identifiant.

        :param permission_id: Identifiant de la permission.
        :returns: La permission ou ``None`` si elle n'existe pas.
        """
        ...

    def get_by_name(self, name: PermissionName) -> Permission | None:
        """Récupère une permission par son nom.

        :param name: Nom de la permission.
        :returns: La permission ou ``None`` si elle n'existe pas.
        """
        ...

    def save(self, permission: Permission) -> None:
        """Sauvegarde une permission (création ou mise à jour).

        :param permission: Permission à sauvegarder.
        """
        ...

    def list_all(self) -> list[Permission]:
        """Liste toutes les permissions.

        :returns: Liste des permissions.
        """
        ...
