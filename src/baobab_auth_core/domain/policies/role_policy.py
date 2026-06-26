"""Politique de gestion des rôles.

:spec: BL-010-004
"""

from dataclasses import dataclass, field

from baobab_auth_core.domain.value_objects.role_name import RoleName

_DEFAULT_ROLE = "USER"
_SUPER_ADMIN_ROLE = "SUPER_ADMIN"


@dataclass(frozen=True)
class RolePolicy:
    """Politique de gestion des rôles et de la hiérarchie.

    :param default_role_name: Rôle attribué automatiquement à tout nouvel utilisateur
        (défaut : ``USER``).
    :param super_admin_role_name: Nom du rôle super-administrateur
        (défaut : ``SUPER_ADMIN``).
    :param enforce_last_super_admin: Interdit la suppression du dernier super-admin
        (défaut : True).
    """

    default_role_name: RoleName = field(default_factory=lambda: RoleName(_DEFAULT_ROLE))
    super_admin_role_name: RoleName = field(
        default_factory=lambda: RoleName(_SUPER_ADMIN_ROLE)
    )
    enforce_last_super_admin: bool = field(default=True)
