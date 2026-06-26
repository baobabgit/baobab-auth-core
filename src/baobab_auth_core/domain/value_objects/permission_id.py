"""Value object PermissionId — identifiant unique d'une permission.

:spec: BL-010-002
"""

from dataclasses import dataclass

from baobab_auth_core.exceptions.validation import ValidationError


@dataclass(frozen=True)
class PermissionId:
    """Identifiant unique d'une permission.

    Refuse les valeurs vides ou contenant uniquement des espaces.

    :param value: Valeur de l'identifiant.
    :raises ValidationError: Si la valeur est vide.
    """

    value: str

    def __post_init__(self) -> None:
        """Valide que la valeur n'est pas vide.

        :raises ValidationError: Si vide.
        """
        if not self.value.strip():
            raise ValidationError("PermissionId ne peut pas être vide.")

    def __str__(self) -> str:
        """Retourne la valeur de l'identifiant.

        :returns: Valeur du PermissionId.
        """
        return self.value

    def __repr__(self) -> str:
        """Représentation lisible.

        :returns: Représentation du PermissionId.
        """
        return f"PermissionId(value={self.value!r})"
