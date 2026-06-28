# FEAT-030.4 — Stabiliser AssignRole

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-030](../user_stories/US-030.md) |
| Backlog | [BL-030-004](../backlogs/BL-030-004.md) |
| Priorité | P0 |
| Statut | DONE ✅ |
| Spec dérivée | [`FEAT-030.4`](../../specifications/us/US-030-rbac-authorization/FEAT-030.4-assign-role.rst) |

## Livrables

Commande et cas d'usage `AssignRole` avec audit `ROLE_ASSIGNED`.

## Critères d'acceptation

- Vérifie acteur, cible et rôle.
- Autorise `ADMIN` ou `SUPER_ADMIN` en v0.3.0.
- L'assignation est idempotente.
- Produit un audit sans secret et commit atomiquement.
