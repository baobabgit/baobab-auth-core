"""Value object RoleName — nom de rôle validé.

:spec: BL-010-002
"""

from dataclasses import dataclass

from baobab_auth_core.exceptions.validation import InvalidRoleNameError


@dataclass(frozen=True)
class RoleName:
    """Nom de rôle normalisé en majuscules.

    Refuse les valeurs vides et celles contenant des espaces.

    :param value: Nom du rôle (ex. ``USER``, ``SUPER_ADMIN``).
    :raises InvalidRoleNameError: Si vide ou contenant des espaces.
    """

    value: str

    def __post_init__(self) -> None:
        """Valide le nom du rôle.

        :raises InvalidRoleNameError: Si invalide.
        """
        stripped = self.value.strip()
        if not stripped:
            raise InvalidRoleNameError("Le nom de rôle ne peut pas être vide.")
        if " " in stripped:
            raise InvalidRoleNameError(
                f"Le nom de rôle ne peut pas contenir d'espaces : '{stripped}'"
            )
        object.__setattr__(self, "value", stripped.upper())

    def __str__(self) -> str:
        """Retourne le nom du rôle.

        :returns: Nom du rôle en majuscules.
        """
        return self.value

    def __repr__(self) -> str:
        """Représentation lisible.

        :returns: Représentation du RoleName.
        """
        return f"RoleName(value={self.value!r})"
