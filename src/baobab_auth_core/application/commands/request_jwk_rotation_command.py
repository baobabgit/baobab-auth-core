"""Commande RequestJwkRotationCommand — demande de rotation des clés JWK.

:spec: BL-040-008
"""

from dataclasses import dataclass

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject


@dataclass(frozen=True)
class RequestJwkRotationCommand:
    """Données d'entrée du cas d'usage ``RequestJwkRotation``.

    :param actor_subject: Sujet de l'acteur (doit être ``SUPER_ADMIN``).
    :param reason: Motif optionnel de la demande (sans secret).
    :param ip_address: Adresse IP de la requête (audit).
    :param user_agent: User-Agent de la requête (audit).
    """

    actor_subject: AuthSubject | str
    reason: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
