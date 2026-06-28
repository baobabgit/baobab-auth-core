# FEAT-050.7 — Tests contractuels inter-briques

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-050](../user_stories/US-050.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-050.7`](../../specifications/us/US-050-stabilisation-contrats/) |

## Livrables

``tests/contracts/{database,security,api,client,admin}/`` validant les contrats publics sans importer d'autre brique.

## Critères d'acceptation

- Les tests de contrat n'importent que ``baobab_auth_core`` (jamais database/security/api/client/admin).
