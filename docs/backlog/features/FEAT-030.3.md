# FEAT-030.3 — Finaliser ports, policies et fakes RBAC

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-030](../user_stories/US-030.md) |
| Backlog | [BL-030-003](../backlogs/BL-030-003.md) |
| Priorité | P0 |
| Statut | TODO |
| Spec dérivée | [`FEAT-030.3`](../../specifications/us/US-030-rbac-authorization/FEAT-030.3-ports-policies-fakes.rst) |

## Livrables

Ports RBAC finalisés, `RolePolicy` renforcée, `PermissionPolicy`, repositories
in-memory utilisables en tests.

## Critères d'acceptation

- `RoleRepository` expose `get_by_name`, `list_roles`, `save`, `count_users_with_role`.
- `PermissionRepository` expose `get_by_name`, `list_permissions`, `save`.
- `RolePolicy` protège le dernier `SUPER_ADMIN`.
- `PermissionPolicy` valide le format métier des permissions.
- Les fakes RBAC restent déterministes et sans dépendance technique.
