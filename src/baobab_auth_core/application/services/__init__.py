"""Services applicatifs (orchestration transverse et autorisation).

:spec: BL-020-002 / BL-030-002
"""

from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService as AuthorizationService,
)

__all__ = ["AuthorizationService"]
