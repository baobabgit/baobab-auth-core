"""Cas d'usage ListPermissions — liste des permissions connues.

:spec: BL-050-007
"""

from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.ports.permission_repository import PermissionRepository


class ListPermissions:
    """Liste les permissions connues du système. Lecture pure, sans audit."""

    def __init__(self, permissions: PermissionRepository) -> None:
        """Initialise le cas d'usage.

        :param permissions: Dépôt de permissions.
        """
        self._permissions = permissions

    def execute(self) -> tuple[Permission, ...]:
        """Retourne toutes les permissions.

        :returns: Tuple des permissions connues.
        """
        return tuple(self._permissions.list_all())
