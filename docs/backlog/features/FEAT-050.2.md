# FEAT-050.2 — DTO applicatifs stabilisés

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-050](../user_stories/US-050.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-050.2`](../../specifications/us/US-050-stabilisation-contrats/) |

## Livrables

``AuthenticatedUser`` (roles + permissions, sans secret), ``SessionDTO``, ``TokenPair``, ``TokenClaims`` et nouveau ``TokenIssueContext``.

## Critères d'acceptation

- ``AuthenticatedUser`` expose ``roles`` et ``permissions``, jamais de secret.
- ``TokenIssueContext`` fournit subject/user_id/session_id/roles/permissions/issued_at/access_expires_at/refresh_expires_at/issuer/audience.
