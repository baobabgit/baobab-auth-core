"""Catalogue d'autorisation par défaut — rôles, permissions et mapping système.

:spec: BL-040-001, BL-040-002, BL-040-003, BL-040-004
"""

from collections.abc import Mapping
from datetime import UTC, datetime

from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName

_SYSTEM_TS = datetime(2024, 1, 1, tzinfo=UTC)

# (name, resource, action, description) — ordre déterministe.
_PERMISSIONS: tuple[tuple[str, str, str, str], ...] = (
    ("auth:user:read", "user", "read", "Lire un compte utilisateur."),
    ("auth:user:write", "user", "write", "Créer ou modifier un compte utilisateur."),
    ("auth:user:disable", "user", "disable", "Désactiver un compte utilisateur."),
    ("auth:role:read", "role", "read", "Lire les rôles."),
    ("auth:role:write", "role", "write", "Créer ou modifier des rôles."),
    ("auth:session:read", "session", "read", "Lire les sessions."),
    ("auth:session:revoke", "session", "revoke", "Révoquer des sessions."),
    ("auth:audit:read", "audit", "read", "Lire le journal d'audit."),
    ("auth:jwk:read", "jwk", "read", "Lire les clés JWK publiques."),
    ("auth:jwk:rotate", "jwk", "rotate", "Déclencher la rotation des clés JWK."),
)

_ROLE_PERMISSIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("USER", ("auth:user:read", "auth:session:read")),
    (
        "ADMIN",
        (
            "auth:user:read",
            "auth:user:write",
            "auth:user:disable",
            "auth:role:read",
            "auth:session:read",
            "auth:session:revoke",
            "auth:audit:read",
            "auth:jwk:read",
        ),
    ),
    ("SERVICE", ()),
    ("SUPER_ADMIN", tuple(name for name, _, _, _ in _PERMISSIONS)),
)


class DefaultAuthCatalog:
    """Catalogue système immuable des rôles, permissions et de leur mapping.

    Aucune I/O, aucune variable d'environnement : les collections sont codées en
    dur dans le domaine et exposées dans un ordre déterministe. Les permissions
    et rôles portent ``is_system=True``.

    :spec: BL-040-001
    """

    def permissions(self) -> tuple[Permission, ...]:
        """Retourne les permissions système, dans l'ordre déterministe.

        :returns: Les 10 permissions ``auth:*`` du catalogue.
        """
        return tuple(
            Permission(
                id=PermissionId(f"perm-{name.replace(':', '-')}"),
                name=PermissionName(name),
                resource=resource,
                action=action,
                is_system=True,
                created_at=_SYSTEM_TS,
                description=description,
            )
            for name, resource, action, description in _PERMISSIONS
        )

    def roles(self) -> tuple[Role, ...]:
        """Retourne les rôles système, dans l'ordre déterministe.

        :returns: Les 4 rôles système (USER, ADMIN, SERVICE, SUPER_ADMIN).
        """
        return tuple(
            Role(
                id=RoleId(f"role-{name.lower()}"),
                name=RoleName(name),
                is_system=True,
                created_at=_SYSTEM_TS,
                updated_at=_SYSTEM_TS,
                description=f"Rôle système {name}.",
                permission_names=tuple(
                    PermissionName(perm) for perm in permission_names
                ),
            )
            for name, permission_names in _ROLE_PERMISSIONS
        )

    def role_permissions(self) -> Mapping[RoleName, tuple[PermissionName, ...]]:
        """Retourne le mapping rôle → permissions.

        :returns: Mapping immuable des rôles système vers leurs permissions.
        """
        return {
            RoleName(name): tuple(PermissionName(perm) for perm in permission_names)
            for name, permission_names in _ROLE_PERMISSIONS
        }
