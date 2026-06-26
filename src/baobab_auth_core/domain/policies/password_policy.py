"""Politique de mot de passe.

:spec: BL-010-004
"""

from dataclasses import dataclass, field

from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
from baobab_auth_core.exceptions.validation import WeakPasswordError

_DEFAULT_MIN_LENGTH = 12
_DEFAULT_MAX_LENGTH = 256


@dataclass(frozen=True)
class PasswordPolicy:
    """Politique de validation des mots de passe.

    Les valeurs par défaut correspondent au niveau de sécurité minimal
    recommandé par OWASP.

    :param min_length: Longueur minimale (défaut : 12).
    :param max_length: Longueur maximale (défaut : 256).
    :param require_letter: Exige au moins une lettre (défaut : True).
    :param require_digit_or_symbol: Exige au moins un chiffre ou symbole
        (défaut : True).
    :param forbid_email_as_password: Interdit l'email comme mot de passe
        (défaut : True).
    """

    min_length: int = field(default=_DEFAULT_MIN_LENGTH)
    max_length: int = field(default=_DEFAULT_MAX_LENGTH)
    require_letter: bool = field(default=True)
    require_digit_or_symbol: bool = field(default=True)
    forbid_email_as_password: bool = field(default=True)

    def validate(
        self,
        password: PlainPassword,
        email: Email | None = None,
    ) -> None:
        """Valide un mot de passe selon la politique.

        :param password: Mot de passe en clair à valider.
        :param email: Adresse email de l'utilisateur (pour la règle d'exclusion).
        :raises WeakPasswordError: Si le mot de passe ne respecte pas la politique.
        """
        value = password.value

        if len(value) < self.min_length:
            raise WeakPasswordError(
                f"Le mot de passe doit contenir au moins {self.min_length} caractères."
            )

        if len(value) > self.max_length:
            raise WeakPasswordError(
                f"Le mot de passe ne peut pas dépasser {self.max_length} caractères."
            )

        if self.require_letter and not any(c.isalpha() for c in value):
            raise WeakPasswordError(
                "Le mot de passe doit contenir au moins une lettre."
            )

        if self.require_digit_or_symbol and not any(
            c.isdigit() or not c.isalnum() for c in value
        ):
            raise WeakPasswordError(
                "Le mot de passe doit contenir au moins un chiffre ou un symbole."
            )

        if (
            self.forbid_email_as_password
            and email is not None
            and value.strip().lower() == email.value
        ):
            raise WeakPasswordError(
                "Le mot de passe ne peut pas être identique à l'adresse email."
            )
