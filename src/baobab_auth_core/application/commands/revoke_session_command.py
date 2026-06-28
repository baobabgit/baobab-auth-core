"""Commande RevokeSessionCommand — révocation d'une session.

:spec: BL-020-006
"""

from dataclasses import dataclass

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.session_id import SessionId


@dataclass(frozen=True)
class RevokeSessionCommand:
    """Données d'entrée du cas d'usage ``RevokeSession``.

    En v0.2.0 l'acteur est minimal (``AuthSubject``) ; le contrôle d'autorisation
    fin par ``AuthContext`` est reporté à v0.3.0 (voir ADR-0008).

    :param actor_subject: Sujet de l'acteur de la révocation (ou None pour système).
    :param session_id: Identifiant de la session à révoquer.
    """

    actor_subject: AuthSubject | None
    session_id: SessionId
