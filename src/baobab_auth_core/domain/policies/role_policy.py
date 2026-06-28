"""Politique de gestion des rôles.

:spec: BL-010-004, BL-040-005, BL-040-006
"""

from collections.abc import Iterable
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

    def is_super_admin_role(self, role: RoleName) -> bool:
        """Indique si un rôle est le rôle super-administrateur.

        :param role: Rôle à tester.
        :returns: ``True`` si ``role`` est le rôle super-admin.
        :spec: BL-040-005
        """
        return role == self.super_admin_role_name

    def can_assign_role(
        self,
        actor_roles: Iterable[RoleName],
        role: RoleName,
    ) -> bool:
        """Indique si un acteur peut attribuer un rôle donné.

        Seul un ``SUPER_ADMIN`` peut attribuer ``SUPER_ADMIN`` ; les autres rôles
        sont attribuables par tout acteur autorisé en amont.

        :param actor_roles: Rôles portés par l'acteur.
        :param role: Rôle à attribuer.
        :returns: ``True`` si l'attribution est autorisée pour cet acteur.
        :spec: BL-040-005
        """
        if not self.is_super_admin_role(role):
            return True
        return self._actor_is_super_admin(actor_roles)

    def can_remove_role(
        self,
        actor_roles: Iterable[RoleName],
        role: RoleName,
    ) -> bool:
        """Indique si un acteur peut retirer un rôle donné.

        Seul un ``SUPER_ADMIN`` peut retirer ``SUPER_ADMIN``.

        :param actor_roles: Rôles portés par l'acteur.
        :param role: Rôle à retirer.
        :returns: ``True`` si le retrait est autorisé pour cet acteur.
        :spec: BL-040-006
        """
        if not self.is_super_admin_role(role):
            return True
        return self._actor_is_super_admin(actor_roles)

    def permits_last_super_admin_removal(
        self,
        role_name: RoleName,
        users_with_role: int,
    ) -> bool:
        """Indique si le retrait respecte la protection du dernier super-admin.

        :param role_name: Nom du rôle à retirer.
        :param users_with_role: Nombre d'utilisateurs portant ce rôle.
        :returns: ``True`` si le retrait ne supprime pas le dernier super-admin.
        :spec: BL-040-006
        """
        if not self.enforce_last_super_admin:
            return True
        if role_name != self.super_admin_role_name:
            return True
        return users_with_role > 1

    def _actor_is_super_admin(self, actor_roles: Iterable[RoleName]) -> bool:
        """Indique si l'acteur porte le rôle super-administrateur.

        :param actor_roles: Rôles portés par l'acteur.
        :returns: ``True`` si l'acteur est super-admin.
        """
        return self.super_admin_role_name in tuple(actor_roles)
