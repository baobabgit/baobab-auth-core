"""Fake TokenProvider — génération de tokens déterministe pour les tests.

:spec: BL-010-007
"""

from typing import Any

from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.exceptions.auth import TokenExpiredError, TokenInvalidError

_FAKE_PREFIX = "fake-token:"
_EXPIRED_MARKER = "EXPIRED"
_INVALID_MARKER = "INVALID"


class FakeTokenProvider:
    """Fournisseur de tokens déterministe pour les tests.

    Les tokens générés sont de simples chaînes prévisibles.
    Les tokens invalides et expirés peuvent être simulés via des marqueurs.
    """

    def __init__(self) -> None:
        """Initialise le fournisseur avec un compteur à zéro."""
        self._counter = 0

    def generate_token_id(self) -> TokenId:
        """Génère un TokenId unique incrémental.

        :returns: TokenId de la forme ``token-id-<n>``.
        """
        self._counter += 1
        return TokenId(f"token-id-{self._counter}")

    def create_access_token(
        self,
        subject: str,
        ttl_seconds: int,
        claims: dict[str, Any] | None = None,
    ) -> str:
        """Crée un token d'accès fake.

        :param subject: Sujet du token.
        :param ttl_seconds: Durée de vie (ignorée dans le fake).
        :param claims: Claims additionnels (ignorés dans le fake).
        :returns: Token fake de la forme ``fake-token:<subject>``.
        """
        _ = ttl_seconds
        _ = claims
        return f"{_FAKE_PREFIX}{subject}"

    def verify_access_token(self, token: str) -> dict[str, Any]:
        """Vérifie un token fake.

        :param token: Token à vérifier.
        :returns: Payload avec le sujet extrait.
        :raises TokenExpiredError: Si le token contient le marqueur ``EXPIRED``.
        :raises TokenInvalidError: Si le token ne commence pas par le préfixe fake
            ou contient le marqueur ``INVALID``.
        """
        if _EXPIRED_MARKER in token:
            raise TokenExpiredError("Token fake expiré.")
        if not token.startswith(_FAKE_PREFIX) or _INVALID_MARKER in token:
            raise TokenInvalidError("Token fake invalide.")
        subject = token[len(_FAKE_PREFIX) :]
        return {"sub": subject}
