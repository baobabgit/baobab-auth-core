"""Politique de validation des permissions RBAC.

:spec: BL-030-003
"""

from dataclasses import dataclass

from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.exceptions.validation import InvalidPermissionNameError


@dataclass(frozen=True)
class PermissionPolicy:
    """Politique de validation des noms de permissions.

    Le format attendu est ``scope:resource:action`` avec trois segments non vides.

    :param separator: Séparateur des segments de permission.
    """

    separator: str = ":"

    def validate(self, permission_name: PermissionName | str) -> None:
        """Valide une permission selon la politique RBAC.

        :param permission_name: Permission à valider.
        :raises InvalidPermissionNameError: Si la permission est invalide.
        """
        if isinstance(permission_name, PermissionName):
            PermissionName(permission_name.value)
            return
        PermissionName(permission_name)

    def is_valid(self, permission_name: PermissionName | str) -> bool:
        """Indique si une permission respecte la politique.

        :param permission_name: Permission à vérifier.
        :returns: ``True`` si la permission est valide.
        """
        try:
            self.validate(permission_name)
        except InvalidPermissionNameError:
            return False
        return True
