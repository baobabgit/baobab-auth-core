# FEAT-050.6 — Cas d'usage admin métier

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-050](../user_stories/US-050.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-050.6`](../../specifications/us/US-050-stabilisation-contrats/) |

## Livrables

``DisableUser``, ``EnableUser``, ``BootstrapSuperAdmin``, ``RequestJwkRotation``.

## Critères d'acceptation

- ``DisableUser``/``EnableUser`` audités (``ACCOUNT_DISABLED``/``ACCOUNT_ENABLED``), réservés ADMIN/SUPER_ADMIN.
- ``BootstrapSuperAdmin`` n'opère que s'il n'existe aucun SUPER_ADMIN (bootstrap système).
