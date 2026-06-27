"""Exceptions liées aux sessions.

:spec: BL-010-005
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class SessionNotFoundError(BaobabAuthCoreError):
    """Session introuvable.

    :param message: Description de l'erreur.
    """


class SessionExpiredError(BaobabAuthCoreError):
    """La session a expiré.

    :param message: Description de l'erreur.
    """


class SessionRevokedError(BaobabAuthCoreError):
    """La session a été révoquée explicitement.

    :param message: Description de l'erreur.
    """
