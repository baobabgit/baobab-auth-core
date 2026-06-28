"""Types d'événements d'audit.

:spec: BL-010-004
"""

from enum import StrEnum


class AuditEventType(StrEnum):
    """Catalogue des types d'événements traçables.

    :cvar USER_REGISTERED: Nouvel utilisateur enregistré.
    :cvar LOGIN_SUCCESS: Connexion réussie.
    :cvar LOGIN_FAILURE: Échec de connexion (identifiants invalides).
    :cvar LOGOUT: Déconnexion explicite.
    :cvar SESSION_REFRESHED: Token de session renouvelé.
    :cvar SESSION_REVOKED: Session révoquée.
    :cvar ROLE_ASSIGNED: Rôle attribué à un utilisateur.
    :cvar ROLE_REMOVED: Rôle retiré d'un utilisateur.
    :cvar PASSWORD_CHANGED: Mot de passe modifié.
    :cvar ACCOUNT_LOCKED: Compte verrouillé suite à trop d'échecs.
    :cvar ACCOUNT_DISABLED: Compte désactivé par un administrateur.
    :cvar ACCOUNT_ENABLED: Compte réactivé par un administrateur.
    :cvar ACCOUNT_DELETED: Compte supprimé.
    :cvar ALL_SESSIONS_REVOKED: Toutes les sessions d'un utilisateur révoquées.
    :cvar JWK_ROTATION_REQUESTED: Demande de rotation des clés JWK (critique).
    """

    USER_REGISTERED = "USER_REGISTERED"
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILURE = "LOGIN_FAILURE"
    LOGOUT = "LOGOUT"
    SESSION_REFRESHED = "SESSION_REFRESHED"
    SESSION_REVOKED = "SESSION_REVOKED"
    ALL_SESSIONS_REVOKED = "ALL_SESSIONS_REVOKED"
    ROLE_ASSIGNED = "ROLE_ASSIGNED"
    ROLE_REMOVED = "ROLE_REMOVED"
    PASSWORD_CHANGED = "PASSWORD_CHANGED"  # nosec B105
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
    ACCOUNT_ENABLED = "ACCOUNT_ENABLED"
    ACCOUNT_DELETED = "ACCOUNT_DELETED"
    JWK_ROTATION_REQUESTED = "JWK_ROTATION_REQUESTED"
