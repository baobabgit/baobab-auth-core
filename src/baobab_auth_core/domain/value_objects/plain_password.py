"""Value object PlainPassword — mot de passe en clair masqué dans les logs.

:spec: BL-010-002
"""

from dataclasses import dataclass

from baobab_auth_core.exceptions.validation import ValidationError


@dataclass(frozen=True)
class PlainPassword:
    """Mot de passe en clair, jamais affiché dans les logs ou repr.

    La valeur est masquée dans :meth:`__repr__` et :meth:`__str__`
    pour éviter toute fuite accidentelle.

    :param value: Mot de passe en clair.
    :raises ValidationError: Si la valeur est vide.
    """

    value: str

    def __post_init__(self) -> None:
        """Valide que le mot de passe n'est pas vide.

        :raises ValidationError: Si vide.
        """
        if not self.value:
            raise ValidationError("Le mot de passe ne peut pas être vide.")

    def __str__(self) -> str:
        """Retourne une représentation masquée.

        :returns: Chaîne masquée.
        """
        return "***"

    def __repr__(self) -> str:
        """Retourne une représentation masquée.

        :returns: Représentation masquée sans valeur.
        """
        return "PlainPassword(value='***')"
