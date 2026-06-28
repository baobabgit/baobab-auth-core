"""DTO AuthenticatedUser — projection publique d'un utilisateur authentifié.

:spec: BL-020-007, BL-050-002
"""

from dataclasses import dataclass, field
from datetime import datetime

from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class AuthenticatedUser:
    """Projection immuable et sans secret d'un :class:`User`.

    Ne contient jamais le ``password_hash`` ni aucune donnée sensible. Expose les
    rôles et les permissions agrégées (vides tant qu'aucun contexte RBAC n'est
    fourni).

    :param id: Identifiant de l'utilisateur.
    :param auth_subject: Sujet d'authentification stable.
    :param email: Adresse email normalisée.
    :param status: Statut du compte.
    :param role_names: Rôles assignés.
    :param permissions: Permissions agrégées (vide par défaut).
    :param created_at: Date de création (UTC).
    :param last_login_at: Date de dernière connexion réussie (ou None).
    """

    id: UserId
    auth_subject: AuthSubject
    email: Email
    status: UserStatus
    role_names: tuple[RoleName, ...]
    permissions: tuple[PermissionName, ...] = field(default=())
    created_at: datetime | None = None
    last_login_at: datetime | None = None

    @property
    def roles(self) -> tuple[RoleName, ...]:
        """Alias public des rôles (nom de champ du contrat v0.5.0).

        :returns: Les rôles de l'utilisateur.
        """
        return self.role_names

    @classmethod
    def from_user(
        cls,
        user: User,
        permissions: tuple[PermissionName, ...] = (),
    ) -> "AuthenticatedUser":
        """Construit le DTO à partir d'une entité :class:`User`.

        :param user: Entité utilisateur source.
        :param permissions: Permissions agrégées à exposer (optionnel).
        :returns: Projection publique sans secret.
        """
        return cls(
            id=user.id,
            auth_subject=user.auth_subject,
            email=user.email,
            status=user.status,
            role_names=user.role_names,
            permissions=permissions,
            created_at=user.created_at,
            last_login_at=user.last_login_at,
        )
