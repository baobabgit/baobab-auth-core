# FEAT-020.8 — Ajouter l'audit auth/session

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-020](../user_stories/US-020.md) |
| Priorité | P0/P1 |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-020.8`](../../specifications/us/US-020-authentification-sessions/) |

## Livrables

Production et garde des événements d'audit auth/session.

## Critères d'acceptation

- Émet les 7 événements obligatoires (USER_REGISTERED … SESSION_REVOKED).
- Refuse les métadonnées sensibles (`password`, `*_token`, `secret`, …).
- Aucun secret n'apparaît dans l'audit.
