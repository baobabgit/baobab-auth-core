"""Exceptions liées aux sessions.

:spec: BL-010-005, BL-050-003
"""

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class SessionNotFoundError(BaobabAuthCoreError):
    """Session introuvable."""

    error_code = "auth.session.not_found"
    http_status = 404
    safe_message = "Session introuvable."


class SessionExpiredError(BaobabAuthCoreError):
    """La session a expiré."""

    error_code = "auth.session.expired"
    http_status = 401
    safe_message = "La session a expiré."


class SessionRevokedError(BaobabAuthCoreError):
    """La session a été révoquée explicitement."""

    error_code = "auth.session.revoked"
    http_status = 401
    safe_message = "La session a été révoquée."
