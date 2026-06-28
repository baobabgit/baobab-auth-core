# FEAT-020.7 — Stabiliser les DTO tokens/session

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-020](../user_stories/US-020.md) |
| Priorité | P0/P1 |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-020.7`](../../specifications/us/US-020-authentification-sessions/) |

## Livrables

`TokenPair`, `TokenClaims`, `SessionDTO`, `AuthenticatedUser`.

## Critères d'acceptation

- `TokenPair` masque les tokens dans `repr()`.
- `SessionDTO` ne contient aucun refresh token brut.
- `AuthenticatedUser` n'expose aucun secret (pas de `password_hash`).
