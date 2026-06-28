"""Commande LogoutCommand — déconnexion d'une session.

:spec: BL-020-005
"""

from dataclasses import dataclass

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.session_id import SessionId


@dataclass(frozen=True)
class LogoutCommand:
    """Données d'entrée du cas d'usage ``Logout``.

    :param session_id: Identifiant de la session à déconnecter.
    :param actor_subject: Sujet de l'acteur (doit posséder la session).
    """

    session_id: SessionId
    actor_subject: AuthSubject
