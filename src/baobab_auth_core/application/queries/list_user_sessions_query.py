"""Query ListUserSessionsQuery — liste des sessions d'un utilisateur.

:spec: BL-050-007
"""

from dataclasses import dataclass

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class ListUserSessionsQuery:
    """Paramètres de lecture des sessions actives d'un utilisateur.

    :param actor_subject: Sujet de l'acteur (le propriétaire ou un administrateur).
    :param target_user_id: Utilisateur dont on liste les sessions.
    """

    actor_subject: AuthSubject | str
    target_user_id: UserId | str
