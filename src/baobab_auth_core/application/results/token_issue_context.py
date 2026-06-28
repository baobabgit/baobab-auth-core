"""DTO TokenIssueContext — contexte d'émission de tokens pour la brique security.

:spec: BL-050-002, BL-050-006
"""

from dataclasses import dataclass
from datetime import datetime

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class TokenIssueContext:
    """Données nécessaires à une brique ``security`` pour émettre des tokens.

    Le core ne dépend d'aucun format de token concret : ce DTO décrit *quoi*
    encoder, jamais *comment*. ``sub``=``AuthSubject``, ``sid``=``SessionId``.

    :param subject: Sujet d'authentification (``sub``).
    :param user_id: Identifiant utilisateur.
    :param session_id: Identifiant de session (``sid``).
    :param roles: Rôles du sujet.
    :param permissions: Permissions agrégées du sujet.
    :param issued_at: Date d'émission (UTC).
    :param access_expires_at: Expiration du token d'accès (UTC).
    :param refresh_expires_at: Expiration du refresh token (UTC).
    :param issuer: Émetteur (``iss``) ou None.
    :param audience: Audience(s) (``aud``) ou None.
    """

    subject: AuthSubject
    user_id: UserId
    session_id: SessionId
    roles: tuple[RoleName, ...]
    permissions: tuple[PermissionName, ...]
    issued_at: datetime
    access_expires_at: datetime
    refresh_expires_at: datetime
    issuer: str | None = None
    audience: str | tuple[str, ...] | None = None
