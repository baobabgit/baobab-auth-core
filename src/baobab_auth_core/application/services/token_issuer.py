"""Service TokenIssuer — émet une paire de tokens pour une session.

:spec: BL-020-002
"""

from baobab_auth_core.application.results.token_pair import TokenPair
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.policies.session_policy import SessionPolicy
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.ports.token_provider import TokenProvider

_TOKEN_TYPE = "Bearer"  # nosec B105


class TokenIssuer:
    """Émet une :class:`TokenPair` (access + refresh) pour une session donnée.

    Mutualise la logique d'émission entre ``AuthenticateUser`` et
    ``RefreshSession``. Le token brut n'est jamais persisté côté domaine.
    """

    def __init__(
        self,
        token_provider: TokenProvider,
        session_policy: SessionPolicy | None = None,
    ) -> None:
        """Initialise l'émetteur.

        :param token_provider: Port de génération de tokens.
        :param session_policy: Politique de session (TTL des tokens).
        """
        self._tokens = token_provider
        self._policy = session_policy or SessionPolicy()

    def issue(
        self,
        subject: AuthSubject,
        session: Session,
        roles: tuple[RoleName, ...],
    ) -> TokenPair:
        """Émet une paire de tokens pour le sujet et la session.

        :param subject: Sujet d'authentification.
        :param session: Session active concernée.
        :param roles: Rôles du sujet (exposés en claims).
        :returns: La paire de tokens émise.
        """
        access_ttl = self._policy.access_token_ttl_seconds
        refresh_ttl = self._policy.refresh_token_ttl_seconds
        claims = {
            "sid": str(session.id),
            "roles": [str(role) for role in roles],
        }
        access_token = self._tokens.create_access_token(
            subject=str(subject),
            ttl_seconds=access_ttl,
            claims=claims,
        )
        refresh_token = self._tokens.create_refresh_token(
            subject=str(subject),
            token_id=session.refresh_token_id,
            ttl_seconds=refresh_ttl,
            claims={"sid": str(session.id)},
        )
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=_TOKEN_TYPE,
            expires_in=access_ttl,
            refresh_expires_in=refresh_ttl,
        )
