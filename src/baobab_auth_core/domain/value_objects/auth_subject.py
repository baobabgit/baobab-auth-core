"""Value object AuthSubject — identifiant stable d'un sujet d'authentification.

:spec: BL-010-002
"""

from dataclasses import dataclass

from baobab_auth_core.exceptions.validation import ValidationError


@dataclass(frozen=True)
class AuthSubject:
    """Identifiant stable et unique d'un sujet d'authentification.

    Cet identifiant ne change jamais, même en cas de changement d'email.
    Une valeur vide lève :exc:`ValidationError`.

    :param value: Valeur de l'identifiant (ex. UUID ou chaîne stable).
    :raises ValidationError: Si la valeur est vide.
    """

    value: str

    def __post_init__(self) -> None:
        """Valide que la valeur n'est pas vide.

        :raises ValidationError: Si vide.
        """
        if not self.value.strip():
            raise ValidationError("AuthSubject ne peut pas être vide.")

    def __str__(self) -> str:
        """Retourne la valeur de l'identifiant.

        :returns: Valeur de l'AuthSubject.
        """
        return self.value

    def __repr__(self) -> str:
        """Représentation lisible.

        :returns: Représentation de l'AuthSubject.
        """
        return f"AuthSubject(value={self.value!r})"
