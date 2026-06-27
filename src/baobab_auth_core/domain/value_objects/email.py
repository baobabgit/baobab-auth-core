"""Value object Email — adresse email normalisée.

:spec: BL-010-002
"""

from dataclasses import dataclass

from baobab_auth_core.exceptions.validation import InvalidEmailError


@dataclass(frozen=True)
class Email:
    """Adresse email normalisée en minuscules.

    La valeur est nettoyée (strip + lower) à la construction.
    Une valeur vide ou sans '@' lève :exc:`InvalidEmailError`.

    :param value: Adresse email brute.
    :raises InvalidEmailError: Si l'adresse est vide ou ne contient pas de '@'.
    """

    value: str

    def __post_init__(self) -> None:
        """Valide et normalise l'adresse email.

        :raises InvalidEmailError: Si invalide.
        """
        normalized = self.value.strip().lower()
        if not normalized or "@" not in normalized:
            raise InvalidEmailError(f"Adresse email invalide : '{self.value}'")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        """Retourne la valeur normalisée.

        :returns: Adresse email en minuscules.
        """
        return self.value

    def __repr__(self) -> str:
        """Représentation lisible.

        :returns: Représentation de l'email.
        """
        return f"Email(value={self.value!r})"
