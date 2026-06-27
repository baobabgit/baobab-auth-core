"""Port UserRepository — persistance des utilisateurs.

:spec: BL-010-006
"""

from typing import Protocol, runtime_checkable

from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.user_id import UserId


@runtime_checkable
class UserRepository(Protocol):
    """Protocole de persistance des entités :class:`User`.

    Toutes les opérations sont synchrones pour v0.1.0.
    """

    def get_by_id(self, user_id: UserId) -> User | None:
        """Récupère un utilisateur par son identifiant.

        :param user_id: Identifiant de l'utilisateur.
        :returns: L'utilisateur ou ``None`` s'il n'existe pas.
        """
        ...

    def get_by_email(self, email: Email) -> User | None:
        """Récupère un utilisateur par son adresse email.

        :param email: Adresse email normalisée.
        :returns: L'utilisateur ou ``None`` s'il n'existe pas.
        """
        ...

    def get_by_auth_subject(self, auth_subject: AuthSubject) -> User | None:
        """Récupère un utilisateur par son sujet d'authentification.

        :param auth_subject: Identifiant stable du sujet.
        :returns: L'utilisateur ou ``None`` s'il n'existe pas.
        """
        ...

    def save(self, user: User) -> None:
        """Sauvegarde un utilisateur (création ou mise à jour).

        :param user: Utilisateur à sauvegarder.
        """
        ...

    def delete(self, user_id: UserId) -> None:
        """Supprime un utilisateur par son identifiant.

        :param user_id: Identifiant de l'utilisateur à supprimer.
        """
        ...

    def exists_by_email(self, email: Email) -> bool:
        """Vérifie si un utilisateur avec cet email existe.

        :param email: Adresse email à vérifier.
        :returns: ``True`` si un utilisateur avec cet email existe.
        """
        ...
