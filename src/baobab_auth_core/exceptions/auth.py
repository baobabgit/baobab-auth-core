"""Exceptions liées à l'authentification et aux tokens.

:spec: BL-010-005
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class InvalidCredentialsError(BaobabAuthCoreError):
    """Identifiants invalides (email ou mot de passe incorrect).

    Le message ne doit pas indiquer lequel des deux est incorrect.

    :param message: Message générique sans secret.
    """


class TokenInvalidError(BaobabAuthCoreError):
    """Token invalide (signature incorrecte, format invalide, etc.).

    :param message: Description de l'erreur.
    """


class TokenExpiredError(BaobabAuthCoreError):
    """Token expiré.

    :param message: Description de l'erreur.
    """
