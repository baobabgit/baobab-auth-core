"""Cas d'usage GetUserBySubject — lecture d'un utilisateur par son sujet.

:spec: BL-050-007
"""

from baobab_auth_core.application.queries.get_user_by_subject_query import (
    GetUserBySubjectQuery,
)
from baobab_auth_core.application.results.authenticated_user import AuthenticatedUser
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.exceptions.user import UserNotFoundError
from baobab_auth_core.ports.user_repository import UserRepository


class GetUserBySubject:
    """Retourne la projection publique d'un utilisateur identifié par son sujet.

    Lecture pure : aucune mutation, aucun audit, aucun secret retourné.
    """

    def __init__(self, users: UserRepository) -> None:
        """Initialise le cas d'usage.

        :param users: Dépôt d'utilisateurs.
        """
        self._users = users

    def execute(self, query: GetUserBySubjectQuery) -> AuthenticatedUser:
        """Exécute la lecture.

        :param query: Sujet recherché.
        :returns: Projection publique de l'utilisateur.
        :raises UserNotFoundError: Si aucun utilisateur ne correspond.
        """
        subject = query.auth_subject
        if not isinstance(subject, AuthSubject):
            subject = AuthSubject(subject)
        user = self._users.get_by_auth_subject(subject)
        if user is None:
            raise UserNotFoundError("Utilisateur introuvable.")
        return AuthenticatedUser.from_user(user)
