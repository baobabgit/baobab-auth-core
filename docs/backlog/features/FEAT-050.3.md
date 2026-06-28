# FEAT-050.3 — Codes d'erreurs métier

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-050](../user_stories/US-050.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-050.3`](../../specifications/us/US-050-stabilisation-contrats/) |

## Livrables

Chaque exception publique expose ``error_code``, ``safe_message`` et un ``http_status`` recommandé.

## Critères d'acceptation

- ``InvalidCredentialsError`` → ``auth.credentials.invalid`` (401), ``ForbiddenError`` → ``auth.authorization.forbidden`` (403), etc.
- ``safe_message`` ne divulgue aucun détail sensible.
