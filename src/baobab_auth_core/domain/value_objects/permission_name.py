"""Value object PermissionName — nom de permission au format scope:resource:action.

:spec: BL-010-002
"""

from dataclasses import dataclass

from baobab_auth_core.exceptions.validation import InvalidPermissionNameError

_EXPECTED_PARTS = 3


@dataclass(frozen=True)
class PermissionName:
    """Nom de permission au format ``scope:resource:action``.

    Les trois segments doivent être non vides.

    :param value: Nom de la permission (ex. ``auth:user:read``).
    :raises InvalidPermissionNameError: Si le format est invalide.
    """

    value: str

    def __post_init__(self) -> None:
        """Valide le format ``scope:resource:action``.

        :raises InvalidPermissionNameError: Si invalide.
        """
        parts = self.value.split(":")
        if len(parts) != _EXPECTED_PARTS or any(p.strip() == "" for p in parts):
            raise InvalidPermissionNameError(
                f"Le nom de permission doit respecter le format "
                f"'scope:resource:action' : '{self.value}'"
            )

    def __str__(self) -> str:
        """Retourne la valeur de la permission.

        :returns: Nom de la permission.
        """
        return self.value

    def __repr__(self) -> str:
        """Représentation lisible.

        :returns: Représentation du PermissionName.
        """
        return f"PermissionName(value={self.value!r})"
