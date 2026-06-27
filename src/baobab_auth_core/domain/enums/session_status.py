"""Statut d'une session utilisateur.

:spec: BL-010-004
"""

from enum import StrEnum


class SessionStatus(StrEnum):
    """Cycle de vie d'une session.

    :cvar ACTIVE: Session active et valide.
    :cvar REVOKED: Session révoquée explicitement
        (déconnexion, changement de mot de passe).
    :cvar EXPIRED: Session expirée (TTL dépassé).
    """

    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"
