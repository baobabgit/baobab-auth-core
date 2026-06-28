"""Port TokenProvider — génération et vérification de tokens.

:spec: BL-010-006
"""

from typing import Any, Protocol, runtime_checkable

from baobab_auth_core.domain.value_objects.token_id import TokenId


@runtime_checkable
class TokenProvider(Protocol):
    """Protocole d'abstraction de la gestion des tokens.

    Les implémentations concrètes utilisent JWT, PASETO, etc.
    Ce port garantit que le domaine n'a aucune dépendance sur la librairie de tokens.

    :spec: ADR-0007
    """

    def generate_token_id(self) -> TokenId:
        """Génère un identifiant unique pour un token.

        :returns: Identifiant de token unique.
        """
        ...

    def create_access_token(
        self,
        subject: str,
        ttl_seconds: int,
        claims: dict[str, Any] | None = None,
    ) -> str:
        """Crée un token d'accès signé.

        :param subject: Sujet du token (ex. ``auth_subject``).
        :param ttl_seconds: Durée de vie en secondes.
        :param claims: Claims additionnels optionnels.
        :returns: Token sérialisé (ex. JWT compact).
        """
        ...

    def verify_access_token(self, token: str) -> dict[str, Any]:
        """Vérifie et décode un token d'accès.

        :param token: Token sérialisé à vérifier.
        :returns: Payload décodé.
        :raises TokenInvalidError: Si le token est invalide.
        :raises TokenExpiredError: Si le token est expiré.
        """
        ...

    def create_refresh_token(
        self,
        subject: str,
        token_id: TokenId,
        ttl_seconds: int,
        claims: dict[str, Any] | None = None,
    ) -> str:
        """Crée un token de rafraîchissement signé.

        Le ``token_id`` (``refresh_token_id``) est porté par le token afin de
        pouvoir retrouver la session lors du rafraîchissement. Le token brut
        n'est jamais stocké ni audité.

        :param subject: Sujet du token (ex. ``auth_subject``).
        :param token_id: Identifiant du refresh token (``refresh_token_id``).
        :param ttl_seconds: Durée de vie en secondes.
        :param claims: Claims additionnels optionnels.
        :returns: Token de rafraîchissement sérialisé.
        :spec: ADR-0007
        """
        ...

    def verify_refresh_token(self, token: str) -> dict[str, Any]:
        """Vérifie et décode un token de rafraîchissement.

        :param token: Token de rafraîchissement à vérifier.
        :returns: Payload décodé, contenant au moins ``refresh_token_id``
            (ou ``jti``).
        :raises TokenInvalidError: Si le token est invalide ou révoqué.
        :raises TokenExpiredError: Si le token est expiré.
        :spec: ADR-0007
        """
        ...

    def revoke_token(self, token: str) -> None:
        """Révoque un token (best-effort).

        Les implémentations sans liste de révocation peuvent ne rien faire ;
        l'appelant traite cette opération comme optionnelle.

        :param token: Token à révoquer.
        :spec: ADR-0007
        """
        ...
