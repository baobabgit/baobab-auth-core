# FEAT-040.8 — Durcissements applicatifs (ChangePassword, RevokeAllSessions)

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-040](../user_stories/US-040.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-040.8`](../../specifications/us/US-040-durcissement-rbac/) |

## Livrables

Cas d'usage ``ChangePassword`` et ``RevokeAllSessions`` durcis (créés en 0.4.0).

## Critères d'acceptation

- ``ChangePassword`` : ancien vérifié, nouveau validé et différent, hash via port, révocation autres sessions selon policy, audit ``PASSWORD_CHANGED`` sans secret.
- ``RevokeAllSessions`` : révoque les sessions, protège un ``SUPER_ADMIN`` d'une neutralisation abusive, audit ``ALL_SESSIONS_REVOKED`` avec ``count``.
