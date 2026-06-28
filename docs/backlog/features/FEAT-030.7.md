# FEAT-030.7 — Compléter audit et tests RBAC

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-030](../user_stories/US-030.md) |
| Backlog | [BL-030-007](../backlogs/BL-030-007.md) |
| Priorité | P1 |
| Statut | TODO |
| Spec dérivée | [`FEAT-030.7`](../../specifications/us/US-030-rbac-authorization/FEAT-030.7-rbac-audit-tests.rst) |

## Livrables

Tests unitaires RBAC et vérification d'audit sans fuite de secret.

## Critères d'acceptation

- Couvre l'agrégation multi-rôles et la déduplication des permissions.
- Couvre les refus `require_role` et `require_permission`.
- Couvre assignation et retrait nominaux et idempotents.
- Couvre la protection du dernier `SUPER_ADMIN`.
- Couvre les audits `ROLE_ASSIGNED` et `ROLE_REMOVED` sans secret.
