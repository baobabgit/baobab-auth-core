"""Exceptions de validation des données d'entrée.

:spec: BL-010-005
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class ValidationError(BaobabAuthCoreError):
    """Erreur de validation générique.

    Levée lorsqu'une valeur fournie ne respecte pas les contraintes métier.

    :param message: Description de l'erreur de validation.
    """


class InvalidEmailError(ValidationError):
    """Adresse email invalide ou vide.

    :param message: Description de l'erreur.
    """


class WeakPasswordError(ValidationError):
    """Mot de passe trop faible ou non conforme à la politique.

    :param message: Description de la non-conformité, sans révéler le mot de passe.
    """


class InvalidRoleNameError(ValidationError):
    """Nom de rôle invalide (vide, contenant des espaces, etc.).

    :param message: Description de l'erreur.
    """


class InvalidPermissionNameError(ValidationError):
    """Nom de permission invalide (format attendu : ``scope:resource:action``).

    :param message: Description de l'erreur.
    """
