"""Cas d'usage GetCurrentUser — utilisateur courant avec rôles et permissions.

:spec: BL-050-007
"""

from baobab_auth_core.application.queries.get_current_user_query import (
    GetCurrentUserQuery,
)
from baobab_auth_core.application.results.authenticated_user import AuthenticatedUser
from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.exceptions.user import UserNotFoundError
from baobab_auth_core.ports.user_repository import UserRepository


class GetCurrentUser:
    """Retourne l'utilisateur courant avec ses rôles et permissions agrégées.

    Lecture pure : aucune mutation, aucun audit. Les permissions sont calculées
    par l'``AuthorizationService`` (le client ne les recalcule pas).
    """

    def __init__(
        self,
        users: UserRepository,
        authorization: AuthorizationService,
    ) -> None:
        """Initialise le cas d'usage.

        :param users: Dépôt d'utilisateurs.
        :param authorization: Service d'autorisation (agrégation des permissions).
        """
        self._users = users
        self._authorization = authorization

    def execute(self, query: GetCurrentUserQuery) -> AuthenticatedUser:
        """Exécute la lecture.

        :param query: Sujet courant.
        :returns: Projection publique avec rôles et permissions.
        :raises UserNotFoundError: Si aucun utilisateur ne correspond.
        """
        subject = query.auth_subject
        if not isinstance(subject, AuthSubject):
            subject = AuthSubject(subject)
        context = self._authorization.build_context(subject)
        user = self._users.get_by_auth_subject(subject)
        if user is None:  # pragma: no cover - build_context already raises
            raise UserNotFoundError("Utilisateur introuvable.")
        return AuthenticatedUser.from_user(user, permissions=context.permissions)
