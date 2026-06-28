"""Exceptions de validation des données d'entrée.

:spec: BL-010-005, BL-050-003
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class ValidationError(BaobabAuthCoreError):
    """Erreur de validation générique.

    Levée lorsqu'une valeur fournie ne respecte pas les contraintes métier.
    """

    error_code = "auth.validation.invalid"
    http_status = 400
    safe_message = "Donnée invalide."


class InvalidEmailError(ValidationError):
    """Adresse email invalide ou vide."""

    error_code = "auth.validation.email_invalid"
    http_status = 400
    safe_message = "Adresse email invalide."


class WeakPasswordError(ValidationError):
    """Mot de passe trop faible ou non conforme à la politique."""

    error_code = "auth.validation.weak_password"  # nosec B105
    http_status = 400
    safe_message = "Le mot de passe ne respecte pas la politique de sécurité."


class InvalidRoleNameError(ValidationError):
    """Nom de rôle invalide (vide, contenant des espaces, etc.)."""

    error_code = "auth.validation.role_name_invalid"
    http_status = 400
    safe_message = "Nom de rôle invalide."


class InvalidPermissionNameError(ValidationError):
    """Nom de permission invalide (format attendu : ``scope:resource:action``)."""

    error_code = "auth.validation.permission_name_invalid"
    http_status = 400
    safe_message = "Nom de permission invalide."
