# FEAT-030.1 — Stabiliser AuthContext

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-030](../user_stories/US-030.md) |
| Backlog | [BL-030-001](../backlogs/BL-030-001.md) |
| Priorité | P0 |
| Statut | Ready |
| Spec dérivée | [`FEAT-030.1`](../../specifications/us/US-030-rbac-authorization/FEAT-030.1-auth-context.rst) |

## Livrables

DTO applicatif immutable `AuthContext` et méthodes de vérification de rôles et permissions.

## Critères d'acceptation

- Contient `auth_subject`, `user_id`, `session_id`, `roles`, `permissions`, `authenticated_at`.
- Déduplique rôles et permissions à la construction.
- Fournit `has_role`, `has_any_role`, `has_permission`, `has_any_permission`, `has_all_permissions`.
- N'expose aucun secret et reste compatible avec les intégrateurs de la librairie.
