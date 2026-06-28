# FEAT-020.3 — Implémenter le lockout minimal

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-020](../user_stories/US-020.md) |
| Priorité | P0/P1 |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-020.3`](../../specifications/us/US-020-authentification-sessions/) |

## Livrables

Verrouillage du compte après N échecs consécutifs.

## Critères d'acceptation

- Incrémente `failed_login_count` à chaque échec.
- Verrouille après `max_failed_login_attempts` et produit `ACCOUNT_LOCKED`.
- Réinitialise le compteur en cas de succès.
