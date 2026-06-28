# FEAT-040.3 — Exceptions de rôle harmonisées

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-040](../user_stories/US-040.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-040.3`](../../specifications/us/US-040-durcissement-rbac/) |

## Livrables

``LastSuperAdminRoleRemovalError`` stable + alias rétrocompatible ``LastAdminRoleRemovalError``.

## Critères d'acceptation

- ``LastSuperAdminRoleRemovalError`` exportée.
- Alias ``LastAdminRoleRemovalError`` conservé.
