"""Commande RevokeAllSessionsCommand — révocation de toutes les sessions.

:spec: BL-040-014
"""

from dataclasses import dataclass

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class RevokeAllSessionsCommand:
    """Données d'entrée du cas d'usage ``RevokeAllSessions``.

    :param actor_subject: Sujet de l'acteur déclenchant la révocation.
    :param target_user_id: Utilisateur dont les sessions sont révoquées.
    :param ip_address: Adresse IP de la requête (audit).
    :param user_agent: User-Agent de la requête (audit).
    """

    actor_subject: AuthSubject | str
    target_user_id: UserId | str
    ip_address: str | None = None
    user_agent: str | None = None
