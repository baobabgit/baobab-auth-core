"""Query GetCurrentUserQuery — lecture de l'utilisateur courant (avec RBAC).

:spec: BL-050-007
"""

from dataclasses import dataclass

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject


@dataclass(frozen=True)
class GetCurrentUserQuery:
    """Paramètres de lecture de l'utilisateur courant.

    :param auth_subject: Sujet d'authentification courant.
    """

    auth_subject: AuthSubject | str
