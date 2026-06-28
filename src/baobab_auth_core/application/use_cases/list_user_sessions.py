"""Cas d'usage ListUserSessions — sessions actives d'un utilisateur.

:spec: BL-050-007
"""

from baobab_auth_core.application.queries.list_user_sessions_query import (
    ListUserSessionsQuery,
)
from baobab_auth_core.application.results.session_dto import SessionDTO
from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.authorization import ForbiddenError
from baobab_auth_core.exceptions.user import UserNotFoundError
from baobab_auth_core.ports.session_repository import SessionRepository
from baobab_auth_core.ports.user_repository import UserRepository

_ADMIN_ROLES = (RoleName("ADMIN"), RoleName("SUPER_ADMIN"))


class ListUserSessions:
    """Liste les sessions actives d'un utilisateur.

    L'acteur doit être le propriétaire du compte ou un administrateur. Lecture
    pure (aucun audit) ; les ``SessionDTO`` ne contiennent aucun token brut.
    """

    def __init__(
        self,
        users: UserRepository,
        sessions: SessionRepository,
        authorization: AuthorizationService,
    ) -> None:
        """Initialise le cas d'usage.

        :param users: Dépôt d'utilisateurs.
        :param sessions: Dépôt de sessions.
        :param authorization: Service d'autorisation.
        """
        self._users = users
        self._sessions = sessions
        self._authorization = authorization

    def execute(self, query: ListUserSessionsQuery) -> tuple[SessionDTO, ...]:
        """Exécute la lecture.

        :param query: Acteur et utilisateur cible.
        :returns: Tuple des sessions actives (DTO sans token brut).
        :raises UserNotFoundError: Si la cible n'existe pas.
        :raises ForbiddenError: Si l'acteur n'est ni le propriétaire ni admin.
        """
        context = self._authorization.build_context(query.actor_subject)
        target_id = (
            query.target_user_id
            if isinstance(query.target_user_id, UserId)
            else UserId(query.target_user_id)
        )
        target = self._users.get_by_id(target_id)
        if target is None:
            raise UserNotFoundError(f"Utilisateur cible introuvable : {target_id}.")

        is_self = context.user_id == target.id
        if not is_self and not context.has_any_role(_ADMIN_ROLES):
            raise ForbiddenError("L'acteur ne peut pas lister ces sessions.")

        return tuple(
            SessionDTO.from_session(session)
            for session in self._sessions.get_active_by_user(target.id)
        )
