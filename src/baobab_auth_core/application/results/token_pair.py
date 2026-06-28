"""DTO TokenPair — paire de tokens d'accès et de rafraîchissement.

:spec: BL-020-007
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TokenPair:
    """Paire de tokens émise lors d'une authentification ou d'un rafraîchissement.

    Les valeurs des tokens sont masquées dans :meth:`__repr__` pour éviter toute
    fuite accidentelle dans les logs.

    :param access_token: Token d'accès sérialisé.
    :param refresh_token: Token de rafraîchissement sérialisé.
    :param token_type: Type de token (ex. ``"Bearer"``).
    :param expires_in: Durée de vie du token d'accès en secondes.
    :param refresh_expires_in: Durée de vie du refresh token en secondes.
    """

    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    refresh_expires_in: int

    def __repr__(self) -> str:
        """Représentation masquant les tokens.

        :returns: Représentation sans valeur de token.
        """
        return (
            "TokenPair(access_token='***', refresh_token='***', "
            f"token_type={self.token_type!r}, expires_in={self.expires_in}, "
            f"refresh_expires_in={self.refresh_expires_in})"
        )
