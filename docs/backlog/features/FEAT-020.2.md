# FEAT-020.2 — Implémenter AuthenticateUser

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-020](../user_stories/US-020.md) |
| Priorité | P0/P1 |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-020.2`](../../specifications/us/US-020-authentification-sessions/) |

## Livrables

Cas d'usage `AuthenticateUser` + commande/résultat, émission de session et tokens.

## Critères d'acceptation

- Message d'échec générique, ne divulgue pas l'existence de l'email.
- Vérifie le mot de passe via `PasswordHasher`, refuse `DISABLED`/`DELETED`/`LOCKED`.
- Crée une session active + `refresh_token_id`, émet une `TokenPair` via `TokenProvider`.
- Produit `LOGIN_SUCCESS` / `LOGIN_FAILURE`, commit atomique.
