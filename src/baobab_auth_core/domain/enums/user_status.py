"""Statut d'un compte utilisateur.

:spec: BL-010-004
"""

from enum import StrEnum


class UserStatus(StrEnum):
    """Cycle de vie d'un compte utilisateur.

    :cvar PENDING: Compte créé, en attente de validation.
    :cvar ACTIVE: Compte actif, l'utilisateur peut se connecter.
    :cvar LOCKED: Compte temporairement verrouillé (trop d'échecs de connexion).
    :cvar DISABLED: Compte désactivé par un administrateur.
    :cvar DELETED: Compte supprimé (soft-delete).
    """

    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    LOCKED = "LOCKED"
    DISABLED = "DISABLED"
    DELETED = "DELETED"
