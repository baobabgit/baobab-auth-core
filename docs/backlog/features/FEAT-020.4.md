# FEAT-020.4 — Implémenter RefreshSession

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-020](../user_stories/US-020.md) |
| Priorité | P0/P1 |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-020.4`](../../specifications/us/US-020-authentification-sessions/) |

## Livrables

Cas d'usage `RefreshSession` + extension refresh du port `TokenProvider`.

## Critères d'acceptation

- Vérifie le refresh token via `TokenProvider`, extrait `refresh_token_id`/`jti`.
- Refuse session expirée/révoquée, met à jour `last_used_at`.
- Émet une nouvelle `TokenPair`, produit `SESSION_REFRESHED`.
- Ne stocke ni n'audite jamais le refresh token brut.
