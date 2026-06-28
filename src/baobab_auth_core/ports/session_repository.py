"""Port SessionRepository — persistance des sessions.

:spec: BL-010-006
"""

from typing import Protocol, runtime_checkable

from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId


@runtime_checkable
class SessionRepository(Protocol):
    """Protocole de persistance des entités :class:`Session`."""

    def get_by_id(self, session_id: SessionId) -> Session | None:
        """Récupère une session par son identifiant.

        :param session_id: Identifiant de la session.
        :returns: La session ou ``None`` si elle n'existe pas.
        """
        ...

    def get_by_refresh_token_id(self, refresh_token_id: TokenId) -> Session | None:
        """Récupère une session par l'identifiant de son refresh token.

        Utilisé par ``RefreshSession`` pour retrouver la session à partir du
        ``refresh_token_id`` extrait du token, sans manipuler le token brut.

        :param refresh_token_id: Identifiant du refresh token de la session.
        :returns: La session ou ``None`` si elle n'existe pas.
        :spec: ADR-0007
        """
        ...

    def get_active_by_user(self, user_id: UserId) -> list[Session]:
        """Liste les sessions actives d'un utilisateur.

        :param user_id: Identifiant de l'utilisateur.
        :returns: Liste des sessions actives.
        """
        ...

    def save(self, session: Session) -> None:
        """Sauvegarde une session (création ou mise à jour).

        :param session: Session à sauvegarder.
        """
        ...

    def delete(self, session_id: SessionId) -> None:
        """Supprime une session par son identifiant.

        :param session_id: Identifiant de la session à supprimer.
        """
        ...
