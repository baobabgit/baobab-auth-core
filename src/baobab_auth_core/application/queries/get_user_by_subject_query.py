"""Query GetUserBySubjectQuery — lecture d'un utilisateur par son sujet.

:spec: BL-050-007
"""

from dataclasses import dataclass

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject


@dataclass(frozen=True)
class GetUserBySubjectQuery:
    """Paramètres de lecture d'un utilisateur par ``AuthSubject``.

    :param auth_subject: Sujet d'authentification recherché.
    """

    auth_subject: AuthSubject | str
