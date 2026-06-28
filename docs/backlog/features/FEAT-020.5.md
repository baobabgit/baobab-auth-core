# FEAT-020.5 — Implémenter Logout

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-020](../user_stories/US-020.md) |
| Priorité | P0/P1 |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-020.5`](../../specifications/us/US-020-authentification-sessions/) |

## Livrables

Cas d'usage `Logout` idempotent.

## Critères d'acceptation

- L'utilisateur déconnecte sa propre session, opération idempotente.
- Révoque la session, demande la révocation du token via `TokenProvider` si disponible.
- Produit `LOGOUT`.
