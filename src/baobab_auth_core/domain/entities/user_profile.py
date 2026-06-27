"""Entité UserProfile — profil public d'un utilisateur.

:spec: BL-010-003
"""

from dataclasses import dataclass
from datetime import datetime

from baobab_auth_core.domain.value_objects.user_id import UserId


@dataclass
class UserProfile:
    """Profil public d'un utilisateur, sans aucun secret.

    Cette entité ne contient aucune information d'authentification
    (pas de mot de passe, hash, token ou secret).

    :param user_id: Identifiant de l'utilisateur associé.
    :param display_name: Nom d'affichage public (ou None).
    :param locale: Code de locale BCP-47 (ex. ``fr-FR``) ou None.
    :param timezone: Fuseau horaire IANA (ex. ``Europe/Paris``) ou None.
    :param avatar_url: URL publique de l'avatar (ou None).
    :param created_at: Date de création (UTC).
    :param updated_at: Date de dernière mise à jour (UTC).
    """

    user_id: UserId
    created_at: datetime
    updated_at: datetime
    display_name: str | None = None
    locale: str | None = None
    timezone: str | None = None
    avatar_url: str | None = None
