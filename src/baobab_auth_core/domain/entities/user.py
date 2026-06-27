"""Entité User — compte utilisateur du domaine.

:spec: BL-010-003
"""

from dataclasses import dataclass, field
from datetime import datetime

from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.validation import ValidationError


@dataclass
class User:
    """Compte utilisateur — agrégat racine du domaine d'authentification.

    Invariants :
    - ``email`` obligatoire et normalisé ;
    - ``auth_subject`` obligatoire et stable ;
    - ``password_hash`` jamais vide ;
    - ``failed_login_count >= 0`` ;
    - dates UTC aware ;
    - rôles sans doublon.

    :param id: Identifiant unique de l'utilisateur.
    :param auth_subject: Identifiant stable du sujet d'authentification.
    :param email: Adresse email normalisée.
    :param password_hash: Hash du mot de passe.
    :param status: Statut actuel du compte.
    :param role_names: Rôles assignés (sans doublon).
    :param created_at: Date de création (UTC).
    :param updated_at: Date de dernière mise à jour (UTC).
    :param last_login_at: Date de dernière connexion réussie (UTC ou None).
    :param failed_login_count: Nombre de tentatives de connexion échouées consécutives.
    :param locked_until: Date de fin de verrouillage (UTC ou None).
    """

    id: UserId
    auth_subject: AuthSubject
    email: Email
    password_hash: PasswordHash
    status: UserStatus
    role_names: tuple[RoleName, ...]
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = field(default=None)
    failed_login_count: int = field(default=0)
    locked_until: datetime | None = field(default=None)

    def __post_init__(self) -> None:
        """Valide les invariants à la construction.

        :raises ValidationError: Si ``failed_login_count`` est négatif ou si
            ``role_names`` contient des doublons.
        """
        if self.failed_login_count < 0:
            raise ValidationError(
                "failed_login_count doit être supérieur ou égal à zéro."
            )
        unique = list(dict.fromkeys(self.role_names))
        if len(unique) != len(self.role_names):
            raise ValidationError("role_names ne peut pas contenir de doublons.")

    def activate(self, now: datetime) -> None:
        """Active le compte utilisateur.

        :param now: Horodatage courant (UTC).
        """
        self.status = UserStatus.ACTIVE
        self.updated_at = now

    def disable(self, now: datetime) -> None:
        """Désactive le compte utilisateur.

        :param now: Horodatage courant (UTC).
        """
        self.status = UserStatus.DISABLED
        self.updated_at = now

    def lock(self, until: datetime, now: datetime) -> None:
        """Verrouille le compte jusqu'à une date donnée.

        :param until: Date de fin de verrouillage (UTC).
        :param now: Horodatage courant (UTC).
        """
        self.status = UserStatus.LOCKED
        self.locked_until = until
        self.updated_at = now

    def unlock(self, now: datetime) -> None:
        """Déverrouille le compte et remet le compteur d'échecs à zéro.

        :param now: Horodatage courant (UTC).
        """
        self.status = UserStatus.ACTIVE
        self.locked_until = None
        self.failed_login_count = 0
        self.updated_at = now

    def mark_login_success(self, now: datetime) -> None:
        """Enregistre une connexion réussie et réinitialise le compteur d'échecs.

        :param now: Horodatage courant (UTC).
        """
        self.last_login_at = now
        self.failed_login_count = 0
        self.updated_at = now

    def mark_login_failure(self, now: datetime) -> None:
        """Incrémente le compteur de tentatives de connexion échouées.

        :param now: Horodatage courant (UTC).
        """
        self.failed_login_count += 1
        self.updated_at = now

    def change_password_hash(self, password_hash: PasswordHash, now: datetime) -> None:
        """Remplace le hash de mot de passe.

        :param password_hash: Nouveau hash.
        :param now: Horodatage courant (UTC).
        """
        self.password_hash = password_hash
        self.updated_at = now

    def assign_role(self, role_name: RoleName, now: datetime) -> None:
        """Assigne un rôle si non déjà présent.

        :param role_name: Nom du rôle à assigner.
        :param now: Horodatage courant (UTC).
        """
        if role_name not in self.role_names:
            self.role_names = (*self.role_names, role_name)
            self.updated_at = now

    def remove_role(self, role_name: RoleName, now: datetime) -> None:
        """Retire un rôle de l'utilisateur.

        :param role_name: Nom du rôle à retirer.
        :param now: Horodatage courant (UTC).
        """
        if role_name in self.role_names:
            self.role_names = tuple(r for r in self.role_names if r != role_name)
            self.updated_at = now

    def has_role(self, role_name: RoleName) -> bool:
        """Vérifie si l'utilisateur possède un rôle donné.

        :param role_name: Nom du rôle à vérifier.
        :returns: ``True`` si le rôle est présent.
        """
        return role_name in self.role_names
