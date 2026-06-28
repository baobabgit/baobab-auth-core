"""Exceptions liées aux utilisateurs.

:spec: BL-010-005, BL-050-003
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class UserAlreadyExistsError(BaobabAuthCoreError):
    """Un utilisateur avec les mêmes identifiants existe déjà."""

    error_code = "auth.user.already_exists"
    http_status = 409
    safe_message = "Un compte existe déjà pour ces identifiants."


class UserNotFoundError(BaobabAuthCoreError):
    """Utilisateur introuvable dans le système."""

    error_code = "auth.user.not_found"
    http_status = 404
    safe_message = "Utilisateur introuvable."


class UserDisabledError(BaobabAuthCoreError):
    """Le compte utilisateur est désactivé."""

    error_code = "auth.user.disabled"
    http_status = 403
    safe_message = "Le compte est désactivé."


class UserLockedError(BaobabAuthCoreError):
    """Le compte utilisateur est temporairement verrouillé."""

    error_code = "auth.user.locked"
    http_status = 423
    safe_message = "Le compte est temporairement verrouillé."


class UserDeletedError(BaobabAuthCoreError):
    """Le compte utilisateur a été supprimé."""

    error_code = "auth.user.deleted"
    http_status = 403
    safe_message = "Le compte est supprimé."
