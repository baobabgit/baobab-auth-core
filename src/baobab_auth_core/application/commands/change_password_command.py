"""Commande ChangePasswordCommand — changement de mot de passe.

:spec: BL-040-013
"""

from dataclasses import dataclass

from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject


@dataclass(frozen=True)
class ChangePasswordCommand:
    """Données d'entrée du cas d'usage ``ChangePassword``.

    :param auth_subject: Sujet de l'utilisateur changeant son mot de passe.
    :param old_password: Mot de passe actuel en clair.
    :param new_password: Nouveau mot de passe en clair.
    :param ip_address: Adresse IP de la requête (audit).
    :param user_agent: User-Agent de la requête (audit).
    """

    auth_subject: AuthSubject | str
    old_password: str
    new_password: str
    ip_address: str | None = None
    user_agent: str | None = None
