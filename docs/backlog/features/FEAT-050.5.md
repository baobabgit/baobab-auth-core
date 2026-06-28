# FEAT-050.5 — Cas d'usage de lecture

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-050](../user_stories/US-050.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-050.5`](../../specifications/us/US-050-stabilisation-contrats/) |

## Livrables

``GetUserBySubject``, ``GetCurrentUser``, ``ListRoles``, ``ListPermissions``, ``ListUserSessions``.

## Critères d'acceptation

- Chaque lecture a query + résultat ; aucune mutation, aucun secret retourné.
- ``GetCurrentUser`` agrège rôles et permissions via l'``AuthorizationService``.
