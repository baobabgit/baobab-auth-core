"""DTO TokenClaims — claims décodés d'un token.

:spec: BL-020-007
"""

from dataclasses import dataclass
from datetime import datetime

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId


@dataclass(frozen=True)
class TokenClaims:
    """Claims structurés portés par un token (lecture après vérification).

    :param subject: Sujet d'authentification.
    :param session_id: Session associée (ou None).
    :param token_id: Identifiant du token.
    :param roles: Rôles du sujet.
    :param permissions: Permissions agrégées (vide en v0.2.0, alimenté en v0.3.0).
    :param issued_at: Date d'émission (UTC).
    :param expires_at: Date d'expiration (UTC).
    :param issuer: Émetteur du token (ou None).
    :param audience: Audience(s) du token (ou None).
    """

    subject: AuthSubject
    session_id: SessionId | None
    token_id: TokenId
    roles: tuple[RoleName, ...]
    permissions: tuple[PermissionName, ...]
    issued_at: datetime
    expires_at: datetime
    issuer: str | None = None
    audience: str | tuple[str, ...] | None = None
