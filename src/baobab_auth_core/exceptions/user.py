"""Exceptions liées aux utilisateurs.

:spec: BL-010-005
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class UserAlreadyExistsError(BaobabAuthCoreError):
    """Un utilisateur avec les mêmes identifiants existe déjà.

    :param message: Description de l'erreur.
    """


class UserNotFoundError(BaobabAuthCoreError):
    """Utilisateur introuvable dans le système.

    :param message: Description de l'erreur.
    """


class UserDisabledError(BaobabAuthCoreError):
    """Le compte utilisateur est désactivé.

    :param message: Description de l'erreur.
    """


class UserLockedError(BaobabAuthCoreError):
    """Le compte utilisateur est temporairement verrouillé.

    :param message: Description de l'erreur.
    """


class UserDeletedError(BaobabAuthCoreError):
    """Le compte utilisateur a été supprimé.

    :param message: Description de l'erreur.
    """
