"""Cas d'usage ListRoles — liste des rôles connus.

:spec: BL-050-007
"""

from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.ports.role_repository import RoleRepository


class ListRoles:
    """Liste les rôles connus du système. Lecture pure, sans audit."""

    def __init__(self, roles: RoleRepository) -> None:
        """Initialise le cas d'usage.

        :param roles: Dépôt de rôles.
        """
        self._roles = roles

    def execute(self) -> tuple[Role, ...]:
        """Retourne tous les rôles.

        :returns: Tuple des rôles connus.
        """
        return tuple(self._roles.list_all())
