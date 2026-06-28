# FEAT-020.6 — Implémenter RevokeSession

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-020](../user_stories/US-020.md) |
| Priorité | P0/P1 |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-020.6`](../../specifications/us/US-020-authentification-sessions/) |

## Livrables

Cas d'usage `RevokeSession` (acteur minimal en 0.2.0).

## Critères d'acceptation

- Révoque une session existante, idempotence documentée.
- Produit `SESSION_REVOKED`, n'audite jamais de token brut.
- `AuthContext` complet reporté à 0.3.0 (acteur minimal).
