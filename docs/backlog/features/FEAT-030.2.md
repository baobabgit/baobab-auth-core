# FEAT-030.2 — Implémenter AuthorizationService

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-030](../user_stories/US-030.md) |
| Backlog | [BL-030-002](../backlogs/BL-030-002.md) |
| Priorité | P0 |
| Statut | TODO |
| Spec dérivée | [`FEAT-030.2`](../../specifications/us/US-030-rbac-authorization/FEAT-030.2-authorization-service.rst) |

## Livrables

Service applicatif `AuthorizationService` construisant un `AuthContext` et vérifiant
rôles et permissions.

## Critères d'acceptation

- Charge l'utilisateur, ses rôles et les permissions associées via les ports.
- Ignore les rôles inconnus en v0.3.0 conformément à l'ADR-0009.
- Fournit `build_context`, `has_role`, `has_permission`, `require_role`, `require_permission`.
- Lève des exceptions métier stables en cas de refus.
