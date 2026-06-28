"""Commande BootstrapSuperAdminCommand — amorçage du premier super-admin.

:spec: BL-050-008
"""

from dataclasses import dataclass

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class BootstrapSuperAdminCommand:
    """Données d'entrée du cas d'usage ``BootstrapSuperAdmin``.

    Amorçage système : ne fonctionne que s'il n'existe encore aucun
    ``SUPER_ADMIN``. L'acteur est optionnel (opération système).

    :param target_user_id: Utilisateur promu ``SUPER_ADMIN``.
    :param actor_subject: Sujet de l'acteur système (ou None).
    :param ip_address: Adresse IP de la requête (audit).
    :param user_agent: User-Agent de la requête (audit).
    """

    target_user_id: UserId | str
    actor_subject: AuthSubject | str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
