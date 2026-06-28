# FEAT-040.5 — Sécurisation des metadata d'audit

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-040](../user_stories/US-040.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-040.5`](../../specifications/us/US-040-durcissement-rbac/) |

## Livrables

Garde anti-fuite : aucune clé sensible dans les métadonnées d'audit.

## Critères d'acceptation

- ``password``, ``*_token``, ``secret``, ``*_hash``, ``authorization``, ``cookie``, ``private_key`` rejetés.
