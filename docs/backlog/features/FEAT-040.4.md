# FEAT-040.4 — Audit JWK_ROTATION_REQUESTED

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-040](../user_stories/US-040.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-040.4`](../../specifications/us/US-040-durcissement-rbac/) |

## Livrables

Événement d'audit ``JWK_ROTATION_REQUESTED`` (CRITICAL) et cas d'usage ``RequestJwkRotation`` réservé ``SUPER_ADMIN``.

## Critères d'acceptation

- ``JWK_ROTATION_REQUESTED`` existe et est CRITICAL à l'émission.
- Seul un acteur ``SUPER_ADMIN`` peut déclencher la demande (``ForbiddenError`` sinon).
