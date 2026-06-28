"""DTO RegisterUserResult — résultat de l'inscription d'un utilisateur.

:spec: BL-020-001
"""

from dataclasses import dataclass

from baobab_auth_core.application.results.authenticated_user import AuthenticatedUser


@dataclass(frozen=True)
class RegisterUserResult:
    """Résultat du cas d'usage ``RegisterUser``.

    :param user: Projection publique de l'utilisateur inscrit.
    """

    user: AuthenticatedUser
