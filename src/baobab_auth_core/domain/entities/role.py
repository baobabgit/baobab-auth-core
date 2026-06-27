"""Entité Role — rôle du système d'autorisation.

:spec: BL-010-003
"""

from dataclasses import dataclass, field
from datetime import datetime

from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName


@dataclass
class Role:
    """Rôle du système d'autorisation regroupant un ensemble de permissions.

    :param id: Identifiant unique du rôle.
    :param name: Nom unique du rôle.
    :param is_system: Si ``True``, rôle système non supprimable.
    :param created_at: Date de création (UTC).
    :param updated_at: Date de dernière mise à jour (UTC).
    :param description: Description optionnelle.
    :param permission_names: Permissions associées (sans doublon).
    """

    id: RoleId
    name: RoleName
    is_system: bool
    created_at: datetime
    updated_at: datetime
    description: str | None = field(default=None)
    permission_names: tuple[PermissionName, ...] = field(default_factory=tuple)
