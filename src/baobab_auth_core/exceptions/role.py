"""Exceptions liées aux rôles et permissions.

:spec: BL-010-005, BL-030-006, BL-050-003
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class RoleError(BaobabAuthCoreError):
    """Erreur générique liée aux rôles et permissions RBAC."""

    error_code = "auth.role.error"
    http_status = 400
    safe_message = "Erreur de gestion des rôles."


class RoleNotFoundError(RoleError):
    """Rôle introuvable dans le système."""

    error_code = "auth.role.not_found"
    http_status = 404
    safe_message = "Rôle introuvable."


class PermissionNotFoundError(RoleError):
    """Permission introuvable dans le système."""

    error_code = "auth.permission.not_found"
    http_status = 404
    safe_message = "Permission introuvable."


class LastSuperAdminRoleRemovalError(RoleError):
    """Tentative de suppression du rôle super-admin du dernier super-administrateur.

    Cette exception protège l'invariant d'existence d'au moins un super-administrateur.
    """

    error_code = "auth.role.last_super_admin"
    http_status = 409
    safe_message = "Impossible de retirer le dernier super-administrateur."


LastAdminRoleRemovalError = LastSuperAdminRoleRemovalError
