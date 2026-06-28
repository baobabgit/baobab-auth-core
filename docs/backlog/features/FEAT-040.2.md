# FEAT-040.2 — Règles strictes SUPER_ADMIN

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-040](../user_stories/US-040.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-040.2`](../../specifications/us/US-040-durcissement-rbac/) |

## Livrables

Durcissement de ``AssignRole``/``RemoveRole`` et de ``RolePolicy`` autour du rôle ``SUPER_ADMIN``.

## Critères d'acceptation

- Un acteur non ``SUPER_ADMIN`` ne peut ni attribuer ni retirer ``SUPER_ADMIN`` (``ForbiddenError``).
- Le dernier ``SUPER_ADMIN`` est protégé (``LastSuperAdminRoleRemovalError``).
- ``RolePolicy`` expose ``is_super_admin_role``, ``can_assign_role``, ``can_remove_role``.
