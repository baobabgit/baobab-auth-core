"""Commande RegisterUserCommand — données d'inscription d'un utilisateur.

:spec: BL-020-001
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserCommand:
    """Données d'entrée du cas d'usage ``RegisterUser``.

    :param email: Adresse email brute de l'utilisateur.
    :param password: Mot de passe en clair.
    :param display_name: Nom d'affichage optionnel.
    :param locale: Locale optionnelle.
    :param timezone: Fuseau horaire optionnel.
    :param ip_address: Adresse IP de la requête (audit).
    :param user_agent: User-Agent de la requête (audit).
    """

    email: str
    password: str
    display_name: str | None = None
    locale: str | None = None
    timezone: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
