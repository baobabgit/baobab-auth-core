"""Fake InMemoryUserRepository — dépôt utilisateur en mémoire pour les tests.

:spec: BL-010-007
"""

from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.user_id import UserId


class InMemoryUserRepository:
    """Dépôt utilisateur en mémoire pour les tests unitaires.

    Stocke les entités :class:`User` dans un dictionnaire keyed par ``UserId``.
    """

    def __init__(self) -> None:
        """Initialise le dépôt avec un stockage vide."""
        self._store: dict[str, User] = {}

    def get_by_id(self, user_id: UserId) -> User | None:
        """Récupère un utilisateur par son identifiant.

        :param user_id: Identifiant de l'utilisateur.
        :returns: L'utilisateur ou ``None``.
        """
        return self._store.get(user_id.value)

    def get_by_email(self, email: Email) -> User | None:
        """Récupère un utilisateur par son adresse email.

        :param email: Adresse email normalisée.
        :returns: L'utilisateur ou ``None``.
        """
        for user in self._store.values():
            if user.email == email:
                return user
        return None

    def get_by_auth_subject(self, auth_subject: AuthSubject) -> User | None:
        """Récupère un utilisateur par son sujet d'authentification.

        :param auth_subject: Sujet d'authentification.
        :returns: L'utilisateur ou ``None``.
        """
        for user in self._store.values():
            if user.auth_subject == auth_subject:
                return user
        return None

    def save(self, user: User) -> None:
        """Sauvegarde un utilisateur.

        :param user: Utilisateur à sauvegarder.
        """
        self._store[user.id.value] = user

    def delete(self, user_id: UserId) -> None:
        """Supprime un utilisateur par son identifiant.

        :param user_id: Identifiant de l'utilisateur à supprimer.
        """
        self._store.pop(user_id.value, None)

    def exists_by_email(self, email: Email) -> bool:
        """Vérifie si un utilisateur avec cet email existe.

        :param email: Adresse email à vérifier.
        :returns: ``True`` si un utilisateur avec cet email existe.
        """
        return any(u.email == email for u in self._store.values())

    def clear(self) -> None:
        """Vide le dépôt — utile pour réinitialiser l'état entre deux tests."""
        self._store.clear()
