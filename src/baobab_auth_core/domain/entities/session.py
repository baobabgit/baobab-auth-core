"""Entité Session — session utilisateur active.

:spec: BL-010-003
"""

from dataclasses import dataclass, field
from datetime import datetime

from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId


@dataclass
class Session:
    """Session utilisateur associant un token de rafraîchissement à un utilisateur.

    :param id: Identifiant unique de la session.
    :param user_id: Identifiant de l'utilisateur propriétaire.
    :param refresh_token_id: Identifiant du token de rafraîchissement.
    :param status: Statut courant de la session.
    :param created_at: Date de création (UTC).
    :param expires_at: Date d'expiration (UTC).
    :param revoked_at: Date de révocation (UTC ou None).
    :param last_used_at: Date de dernière utilisation (UTC ou None).
    :param user_agent: User-Agent HTTP du client (ou None).
    :param ip_address: Adresse IP du client (ou None).
    :param device_label: Libellé lisible du device (ou None).
    """

    id: SessionId
    user_id: UserId
    refresh_token_id: TokenId
    status: SessionStatus
    created_at: datetime
    expires_at: datetime
    revoked_at: datetime | None = field(default=None)
    last_used_at: datetime | None = field(default=None)
    user_agent: str | None = field(default=None)
    ip_address: str | None = field(default=None)
    device_label: str | None = field(default=None)
