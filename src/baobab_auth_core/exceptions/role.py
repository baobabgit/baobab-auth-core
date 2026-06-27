"""Exceptions liées aux rôles et permissions.

:spec: BL-010-005
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class RoleNotFoundError(BaobabAuthCoreError):
    """Rôle introuvable dans le système.

    :param message: Description de l'erreur.
    """


class PermissionNotFoundError(BaobabAuthCoreError):
    """Permission introuvable dans le système.

    :param message: Description de l'erreur.
    """


class LastSuperAdminRoleRemovalError(BaobabAuthCoreError):
    """Tentative de suppression du rôle super-admin du dernier super-administrateur.

    Cette exception protège l'invariant d'existence d'au moins un super-administrateur.

    :param message: Description de l'erreur.
    """
