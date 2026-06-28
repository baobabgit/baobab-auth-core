"""Exceptions liées à l'autorisation.

:spec: BL-010-005, BL-050-003
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class AuthorizationError(BaobabAuthCoreError):
    """Erreur d'autorisation générique."""

    error_code = "auth.authorization.error"
    http_status = 403
    safe_message = "Accès refusé."


class ForbiddenError(AuthorizationError):
    """Accès interdit à la ressource demandée."""

    error_code = "auth.authorization.forbidden"
    http_status = 403
    safe_message = "Action non autorisée."


class PermissionDeniedError(AuthorizationError):
    """Permission requise absente pour l'action demandée."""

    error_code = "auth.authorization.permission_denied"
    http_status = 403
    safe_message = "Permission refusée."
