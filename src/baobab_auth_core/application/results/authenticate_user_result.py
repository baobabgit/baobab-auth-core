"""DTO AuthenticateUserResult — résultat d'une authentification réussie.

:spec: BL-020-002
"""

from dataclasses import dataclass

from baobab_auth_core.application.results.authenticated_user import AuthenticatedUser
from baobab_auth_core.application.results.session_dto import SessionDTO
from baobab_auth_core.application.results.token_pair import TokenPair


@dataclass(frozen=True)
class AuthenticateUserResult:
    """Résultat du cas d'usage ``AuthenticateUser``.

    :param user: Projection publique de l'utilisateur authentifié.
    :param session: Projection publique de la session créée.
    :param tokens: Paire de tokens émise.
    """

    user: AuthenticatedUser
    session: SessionDTO
    tokens: TokenPair
