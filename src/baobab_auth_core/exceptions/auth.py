"""Exceptions liées à l'authentification et aux tokens.

:spec: BL-010-005, BL-050-003
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class InvalidCredentialsError(BaobabAuthCoreError):
    """Identifiants invalides (email ou mot de passe incorrect).

    Le message ne doit pas indiquer lequel des deux est incorrect.
    """

    error_code = "auth.credentials.invalid"
    http_status = 401
    safe_message = "Identifiants invalides."


class TokenInvalidError(BaobabAuthCoreError):
    """Token invalide (signature incorrecte, format invalide, etc.)."""

    error_code = "auth.token.invalid"  # nosec B105
    http_status = 401
    safe_message = "Token invalide."


class TokenExpiredError(BaobabAuthCoreError):
    """Token expiré."""

    error_code = "auth.token.expired"  # nosec B105
    http_status = 401
    safe_message = "Token expiré."
