# FEAT-030.6 — Stabiliser exceptions RBAC

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-030](../user_stories/US-030.md) |
| Backlog | [BL-030-006](../backlogs/BL-030-006.md) |
| Priorité | P1 |
| Statut | TODO |
| Spec dérivée | [`FEAT-030.6`](../../specifications/us/US-030-rbac-authorization/FEAT-030.6-rbac-exceptions.rst) |

## Livrables

Hiérarchie d'exceptions RBAC publique et rétrocompatible.

## Critères d'acceptation

- Exporte `AuthorizationError`, `ForbiddenError`, `PermissionDeniedError`, `RoleError`.
- Exporte `RoleNotFoundError`, `PermissionNotFoundError`, `LastSuperAdminRoleRemovalError`.
- Fournit l'alias rétrocompatible `LastAdminRoleRemovalError` si nécessaire.
- Les exceptions publiques ont des docstrings RST et sont incluses dans `__all__`.
