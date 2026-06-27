"""Niveau de sévérité d'un événement d'audit.

:spec: BL-010-004
"""

from enum import StrEnum


class AuditSeverity(StrEnum):
    """Sévérité d'un événement d'audit.

    :cvar INFO: Événement informatif, opération normale.
    :cvar WARNING: Situation anormale mais non critique.
    :cvar CRITICAL: Incident de sécurité ou erreur grave.
    """

    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
