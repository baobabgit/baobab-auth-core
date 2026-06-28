"""DTO SessionDTO — projection publique d'une session.

:spec: BL-020-007
"""

from dataclasses import dataclass
from datetime import datetime

from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class SessionDTO:
    """Projection immuable d'une :class:`Session`, sans refresh token brut.

    :param id: Identifiant de la session.
    :param user_id: Identifiant de l'utilisateur propriétaire.
    :param status: Statut de la session.
    :param created_at: Date de création (UTC).
    :param expires_at: Date d'expiration (UTC).
    :param last_used_at: Date de dernière utilisation (ou None).
    :param ip_address: Adresse IP du client (ou None).
    :param user_agent: User-Agent du client (ou None).
    :param device_label: Libellé du device (ou None).
    """

    id: SessionId
    user_id: UserId
    status: SessionStatus
    created_at: datetime
    expires_at: datetime
    last_used_at: datetime | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    device_label: str | None = None

    @classmethod
    def from_session(cls, session: Session) -> "SessionDTO":
        """Construit le DTO à partir d'une entité :class:`Session`.

        Le ``refresh_token_id`` n'est jamais exposé.

        :param session: Entité session source.
        :returns: Projection publique sans refresh token.
        """
        return cls(
            id=session.id,
            user_id=session.user_id,
            status=session.status,
            created_at=session.created_at,
            expires_at=session.expires_at,
            last_used_at=session.last_used_at,
            ip_address=session.ip_address,
            user_agent=session.user_agent,
            device_label=session.device_label,
        )
