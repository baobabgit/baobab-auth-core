"""Commande RefreshSessionCommand — données de rafraîchissement de session.

:spec: BL-020-004
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RefreshSessionCommand:
    """Données d'entrée du cas d'usage ``RefreshSession``.

    :param refresh_token: Refresh token brut fourni par le client.
    :param ip_address: Adresse IP de la requête (audit).
    :param user_agent: User-Agent de la requête (audit).
    """

    refresh_token: str
    ip_address: str | None = None
    user_agent: str | None = None
