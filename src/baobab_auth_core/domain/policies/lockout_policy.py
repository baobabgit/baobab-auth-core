"""Politique de verrouillage de compte (lockout).

:spec: BL-050-001
"""

from dataclasses import dataclass, field

_DEFAULT_MAX_FAILED_ATTEMPTS = 5
_DEFAULT_LOCKOUT_DURATION = 900


@dataclass(frozen=True)
class LockoutPolicy:
    """Paramètres de verrouillage après échecs de connexion.

    Type de contrat dédié exposé aux briques consommatrices. Les mêmes paramètres
    sont aussi portés par ``SessionPolicy`` (utilisée par ``AuthenticateUser``) ;
    ``LockoutPolicy`` en est la vue dédiée et stable.

    :param max_failed_login_attempts: Nombre maximum d'échecs avant verrouillage
        (défaut : 5).
    :param lockout_duration_seconds: Durée du verrouillage en secondes (défaut : 900).
    """

    max_failed_login_attempts: int = field(default=_DEFAULT_MAX_FAILED_ATTEMPTS)
    lockout_duration_seconds: int = field(default=_DEFAULT_LOCKOUT_DURATION)
