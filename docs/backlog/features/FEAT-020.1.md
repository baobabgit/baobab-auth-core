# FEAT-020.1 — Implémenter RegisterUser

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-020](../user_stories/US-020.md) |
| Priorité | P0/P1 |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-020.1`](../../specifications/us/US-020-authentification-sessions/) |

## Livrables

Cas d'usage `RegisterUser` + `RegisterUserCommand`/`RegisterUserResult`.

## Critères d'acceptation

- Normalise l'email et refuse un email déjà existant (`UserAlreadyExistsError`).
- Valide le mot de passe via `PasswordPolicy` (`WeakPasswordError`).
- Hashe via `PasswordHasher`, génère `UserId`/`AuthSubject` via `IdGenerator`.
- Attribue le rôle `USER` si disponible, produit l'audit `USER_REGISTERED`, commit atomique.
