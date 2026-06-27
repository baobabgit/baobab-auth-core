"""Politique de gestion des sessions.

:spec: BL-010-004
"""

from dataclasses import dataclass, field

_DEFAULT_ACCESS_TOKEN_TTL = 900
_DEFAULT_REFRESH_TOKEN_TTL = 2592000
_DEFAULT_MAX_FAILED_ATTEMPTS = 5
_DEFAULT_LOCKOUT_DURATION = 900


@dataclass(frozen=True)
class SessionPolicy:
    """Politique de durée de vie et de sécurité des sessions.

    :param access_token_ttl_seconds: Durée de vie du token d'accès en secondes
        (défaut : 900).
    :param refresh_token_ttl_seconds: Durée de vie du token de rafraîchissement
        en secondes (défaut : 2 592 000, soit 30 jours).
    :param max_failed_login_attempts: Nombre maximum d'échecs avant verrouillage
        (défaut : 5).
    :param lockout_duration_seconds: Durée du verrouillage en secondes (défaut : 900).
    :param revoke_other_sessions_on_password_change: Révoque les autres sessions
        lors d'un changement de mot de passe (défaut : True).
    """

    access_token_ttl_seconds: int = field(default=_DEFAULT_ACCESS_TOKEN_TTL)
    refresh_token_ttl_seconds: int = field(default=_DEFAULT_REFRESH_TOKEN_TTL)
    max_failed_login_attempts: int = field(default=_DEFAULT_MAX_FAILED_ATTEMPTS)
    lockout_duration_seconds: int = field(default=_DEFAULT_LOCKOUT_DURATION)
    revoke_other_sessions_on_password_change: bool = field(default=True)
