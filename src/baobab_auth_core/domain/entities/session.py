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

    def is_expired(self, now: datetime) -> bool:
        """Indique si la session est expirée à l'instant donné.

        :param now: Horodatage courant (UTC).
        :returns: ``True`` si ``now`` est postérieur ou égal à ``expires_at``
            ou si le statut est déjà ``EXPIRED``.
        :spec: BL-020-004
        """
        return self.status == SessionStatus.EXPIRED or now >= self.expires_at

    def is_active(self, now: datetime) -> bool:
        """Indique si la session est active et utilisable.

        :param now: Horodatage courant (UTC).
        :returns: ``True`` si le statut est ``ACTIVE``, non révoquée et non expirée.
        :spec: BL-020-004
        """
        return (
            self.status == SessionStatus.ACTIVE
            and self.revoked_at is None
            and not self.is_expired(now)
        )

    def mark_used(self, now: datetime) -> None:
        """Met à jour l'horodatage de dernière utilisation.

        :param now: Horodatage courant (UTC).
        :spec: BL-020-004
        """
        self.last_used_at = now

    def rotate_refresh_token(self, refresh_token_id: TokenId, now: datetime) -> None:
        """Remplace l'identifiant du refresh token (rotation) et marque l'usage.

        :param refresh_token_id: Nouveau ``refresh_token_id``.
        :param now: Horodatage courant (UTC).
        :spec: BL-020-004
        """
        self.refresh_token_id = refresh_token_id
        self.last_used_at = now

    def revoke(self, now: datetime) -> None:
        """Révoque la session (idempotent).

        :param now: Horodatage courant (UTC).
        :spec: BL-020-006
        """
        if self.status == SessionStatus.REVOKED:
            return
        self.status = SessionStatus.REVOKED
        self.revoked_at = now

    def expire(self, now: datetime) -> None:
        """Marque la session comme expirée.

        :param now: Horodatage courant (UTC).
        :spec: BL-020-004
        """
        self.status = SessionStatus.EXPIRED
        self.last_used_at = now
