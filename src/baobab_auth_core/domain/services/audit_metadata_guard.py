"""Service AuditMetadataGuard — garde contre la fuite de secrets dans l'audit.

:spec: BL-020-008
"""

from collections.abc import Mapping
from typing import Any

from baobab_auth_core.exceptions.validation import ValidationError

_FORBIDDEN_SUBSTRINGS = frozenset(
    {
        "password",
        "secret",
        "token",
        "private_key",
        "authorization",
        "cookie",
        "hash",
    }
)


class AuditMetadataGuard:
    """Empêche l'inclusion de données sensibles dans les métadonnées d'audit.

    Toute clé dont le nom (insensible à la casse) contient un terme interdit
    (``password``, ``token``, ``secret``, ``hash``, ``authorization``, ``cookie``,
    ``private_key``) est rejetée.
    """

    def ensure_safe(self, metadata: Mapping[str, Any]) -> dict[str, Any]:
        """Valide que les métadonnées ne contiennent aucune clé sensible.

        :param metadata: Métadonnées candidates.
        :returns: Une copie des métadonnées (sûres).
        :raises ValidationError: Si une clé sensible est détectée.
        """
        for key in metadata:
            lowered = key.lower()
            if any(forbidden in lowered for forbidden in _FORBIDDEN_SUBSTRINGS):
                raise ValidationError(
                    "Métadonnée d'audit interdite : une clé sensible a été détectée."
                )
        return dict(metadata)
