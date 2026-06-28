"""DTO RefreshSessionResult — résultat d'un rafraîchissement de session.

:spec: BL-020-004
"""

from dataclasses import dataclass

from baobab_auth_core.application.results.session_dto import SessionDTO
from baobab_auth_core.application.results.token_pair import TokenPair


@dataclass(frozen=True)
class RefreshSessionResult:
    """Résultat du cas d'usage ``RefreshSession``.

    :param session: Projection publique de la session rafraîchie.
    :param tokens: Nouvelle paire de tokens émise.
    """

    session: SessionDTO
    tokens: TokenPair
