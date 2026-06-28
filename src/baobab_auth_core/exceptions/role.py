"""Exceptions liées aux rôles et permissions.

:spec: BL-010-005
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class RoleError(BaobabAuthCoreError):
    """Erreur générique liée aux rôles et permissions RBAC.

    :param message: Description de l'erreur.
    :spec: BL-030-006
    """


class RoleNotFoundError(RoleError):
    """Rôle introuvable dans le système.

    :param message: Description de l'erreur.
    :spec: BL-030-006
    """


class PermissionNotFoundError(RoleError):
    """Permission introuvable dans le système.

    :param message: Description de l'erreur.
    :spec: BL-030-006
    """


class LastSuperAdminRoleRemovalError(RoleError):
    """Tentative de suppression du rôle super-admin du dernier super-administrateur.

    Cette exception protège l'invariant d'existence d'au moins un super-administrateur.

    :param message: Description de l'erreur.
    :spec: BL-030-006
    """


LastAdminRoleRemovalError = LastSuperAdminRoleRemovalError
