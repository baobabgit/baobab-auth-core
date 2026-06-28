"""Commande AuthenticateUserCommand — données d'authentification.

:spec: BL-020-002
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticateUserCommand:
    """Données d'entrée du cas d'usage ``AuthenticateUser``.

    :param email: Adresse email brute.
    :param password: Mot de passe en clair.
    :param ip_address: Adresse IP de la requête (audit, session).
    :param user_agent: User-Agent de la requête (audit, session).
    :param device_label: Libellé lisible du device (session).
    """

    email: str
    password: str
    ip_address: str | None = None
    user_agent: str | None = None
    device_label: str | None = None
