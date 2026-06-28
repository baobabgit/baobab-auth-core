"""Fake TokenProvider — génération de tokens déterministe pour les tests.

:spec: BL-010-007
"""

from typing import Any

from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.exceptions.auth import TokenExpiredError, TokenInvalidError

_FAKE_PREFIX = "fake-token:"
_REFRESH_PREFIX = "fake-refresh:"
_EXPIRED_MARKER = "EXPIRED"
_INVALID_MARKER = "INVALID"


class FakeTokenProvider:
    """Fournisseur de tokens déterministe pour les tests.

    Les tokens générés sont de simples chaînes prévisibles.
    Les tokens invalides et expirés peuvent être simulés via des marqueurs.
    Les refresh tokens portent le ``refresh_token_id`` et peuvent être révoqués.

    :spec: ADR-0007
    """

    def __init__(self) -> None:
        """Initialise le fournisseur avec un compteur à zéro."""
        self._counter = 0
        self._revoked: set[str] = set()

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

    def create_refresh_token(
        self,
        subject: str,
        token_id: TokenId,
        ttl_seconds: int,
        claims: dict[str, Any] | None = None,
    ) -> str:
        """Crée un refresh token fake portant le ``refresh_token_id``.

        :param subject: Sujet du token.
        :param token_id: Identifiant du refresh token.
        :param ttl_seconds: Durée de vie (ignorée dans le fake).
        :param claims: Claims additionnels (ignorés dans le fake).
        :returns: Token de la forme ``fake-refresh:<token_id>:<subject>``.
        """
        _ = ttl_seconds
        _ = claims
        return f"{_REFRESH_PREFIX}{token_id.value}:{subject}"

    def verify_refresh_token(self, token: str) -> dict[str, Any]:
        """Vérifie un refresh token fake.

        :param token: Token à vérifier.
        :returns: Payload contenant ``sub`` et ``refresh_token_id`` (alias ``jti``).
        :raises TokenExpiredError: Si le token contient le marqueur ``EXPIRED``.
        :raises TokenInvalidError: Si le token est mal formé, révoqué ou marqué
            ``INVALID``.
        """
        if _EXPIRED_MARKER in token:
            raise TokenExpiredError("Refresh token fake expiré.")
        if (
            not token.startswith(_REFRESH_PREFIX)
            or _INVALID_MARKER in token
            or token in self._revoked
        ):
            raise TokenInvalidError("Refresh token fake invalide.")
        payload = token[len(_REFRESH_PREFIX) :]
        token_id, _, subject = payload.partition(":")
        return {"sub": subject, "refresh_token_id": token_id, "jti": token_id}

    def revoke_token(self, token: str) -> None:
        """Révoque un token fake en l'ajoutant à la liste de révocation.

        :param token: Token à révoquer.
        """
        self._revoked.add(token)
