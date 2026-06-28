# FEAT-050.4 — Contrats database et security

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-050](../user_stories/US-050.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-050.4`](../../specifications/us/US-050-stabilisation-contrats/) |

## Livrables

Ports repositories, ``PasswordHasher`` et ``TokenProvider`` stabilisés ; ``DefaultAuthCatalog`` utilisable pour le seed.

## Critères d'acceptation

- Aucune connaissance des noms de tables dans le core ; ``AuditEvent.metadata`` JSON-sérialisable ; dates UTC aware.
- ``sub``=AuthSubject, ``jti``=TokenId, ``sid``=SessionId ; pas de JWT/Argon2 concret.
