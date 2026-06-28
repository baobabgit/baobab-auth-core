"""Commande RemoveRoleCommand — données de retrait d'un rôle.

:spec: BL-030-005
"""

from dataclasses import dataclass

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class RemoveRoleCommand:
    """Données d'entrée du cas d'usage ``RemoveRole``.

    :param actor_subject: Sujet d'authentification de l'acteur.
    :param target_user_id: Identifiant de l'utilisateur cible.
    :param role_name: Rôle à retirer.
    :param ip_address: Adresse IP de la requête (audit).
    :param user_agent: User-Agent de la requête (audit).
    :spec: BL-030-005
    """

    actor_subject: AuthSubject | str
    target_user_id: UserId | str
    role_name: RoleName | str
    ip_address: str | None = None
    user_agent: str | None = None
