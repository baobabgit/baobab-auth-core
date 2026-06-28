# FEAT-030.5 — Stabiliser RemoveRole

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-030](../user_stories/US-030.md) |
| Backlog | [BL-030-005](../backlogs/BL-030-005.md) |
| Priorité | P0 |
| Statut | TODO |
| Spec dérivée | [`FEAT-030.5`](../../specifications/us/US-030-rbac-authorization/FEAT-030.5-remove-role.rst) |

## Livrables

Commande et cas d'usage `RemoveRole` avec audit `ROLE_REMOVED`.

## Critères d'acceptation

- Vérifie acteur, cible et rôle.
- Autorise `ADMIN` ou `SUPER_ADMIN` en v0.3.0.
- Le retrait est idempotent si le rôle est absent.
- Protège le dernier `SUPER_ADMIN`.
- Produit un audit sans secret et commit atomiquement.
