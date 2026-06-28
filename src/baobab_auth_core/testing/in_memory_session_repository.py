"""Fake InMemorySessionRepository — dépôt de sessions en mémoire pour les tests.

:spec: BL-010-007
"""

from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId


class InMemorySessionRepository:
    """Dépôt de sessions en mémoire pour les tests unitaires."""

    def __init__(self) -> None:
        """Initialise le dépôt avec un stockage vide."""
        self._store: dict[str, Session] = {}

    def get_by_id(self, session_id: SessionId) -> Session | None:
        """Récupère une session par son identifiant.

        :param session_id: Identifiant de la session.
        :returns: La session ou ``None``.
        """
        return self._store.get(session_id.value)

    def get_by_refresh_token_id(self, refresh_token_id: TokenId) -> Session | None:
        """Récupère une session par l'identifiant de son refresh token.

        :param refresh_token_id: Identifiant du refresh token.
        :returns: La session ou ``None``.
        """
        for session in self._store.values():
            if session.refresh_token_id == refresh_token_id:
                return session
        return None

    def get_active_by_user(self, user_id: UserId) -> list[Session]:
        """Liste les sessions actives d'un utilisateur.

        :param user_id: Identifiant de l'utilisateur.
        :returns: Liste des sessions dont le statut est ``ACTIVE``.
        """
        return [
            s
            for s in self._store.values()
            if s.user_id == user_id and s.status == SessionStatus.ACTIVE
        ]

    def save(self, session: Session) -> None:
        """Sauvegarde une session.

        :param session: Session à sauvegarder.
        """
        self._store[session.id.value] = session

    def delete(self, session_id: SessionId) -> None:
        """Supprime une session par son identifiant.

        :param session_id: Identifiant de la session à supprimer.
        """
        self._store.pop(session_id.value, None)

    def clear(self) -> None:
        """Vide le dépôt."""
        self._store.clear()
