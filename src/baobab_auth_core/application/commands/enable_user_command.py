"""Commande EnableUserCommand — réactivation d'un compte.

:spec: BL-050-008
"""

from dataclasses import dataclass

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class EnableUserCommand:
    """Données d'entrée du cas d'usage ``EnableUser``.

    :param actor_subject: Sujet de l'acteur (ADMIN ou SUPER_ADMIN).
    :param target_user_id: Utilisateur à réactiver.
    :param ip_address: Adresse IP de la requête (audit).
    :param user_agent: User-Agent de la requête (audit).
    """

    actor_subject: AuthSubject | str
    target_user_id: UserId | str
    ip_address: str | None = None
    user_agent: str | None = None
