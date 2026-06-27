"""Exceptions liées à l'autorisation.

:spec: BL-010-005
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class AuthorizationError(BaobabAuthCoreError):
    """Erreur d'autorisation générique.

    :param message: Description de l'erreur.
    """


class ForbiddenError(AuthorizationError):
    """Accès interdit à la ressource demandée.

    :param message: Description de l'erreur.
    """


class PermissionDeniedError(AuthorizationError):
    """Permission requise absente pour l'action demandée.

    :param message: Description de l'erreur.
    """
