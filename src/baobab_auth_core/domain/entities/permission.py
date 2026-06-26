"""Entité Permission — permission atomique du système d'autorisation.

:spec: BL-010-003
"""

from dataclasses import dataclass, field
from datetime import datetime

from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName


@dataclass
class Permission:
    """Permission atomique du système d'autorisation.

    :param id: Identifiant unique de la permission.
    :param name: Nom unique au format ``scope:resource:action``.
    :param resource: Ressource ciblée.
    :param action: Action autorisée sur la ressource.
    :param is_system: Si ``True``, permission système non supprimable.
    :param created_at: Date de création (UTC).
    :param description: Description optionnelle.
    """

    id: PermissionId
    name: PermissionName
    resource: str
    action: str
    is_system: bool
    created_at: datetime
    description: str | None = field(default=None)
