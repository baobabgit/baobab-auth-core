# FEAT-050.1 — Exports publics stabilisés

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-050](../user_stories/US-050.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-050.1`](../../specifications/us/US-050-stabilisation-contrats/) |

## Livrables

API publique exhaustive dans ``baobab_auth_core.__all__`` + tests d'import.

## Critères d'acceptation

- Entités, value objects, enums, policies, catalogues, ports, DTO et use cases exportés.
- Tests d'import vérifiant que chaque symbole de ``__all__`` est importable.
