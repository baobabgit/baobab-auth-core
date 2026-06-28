# FEAT-040.1 — DefaultAuthCatalog (rôles, permissions, mapping)

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-040](../user_stories/US-040.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-040.1`](../../specifications/us/US-040-durcissement-rbac/) |

## Livrables

Catalogue système : 10 permissions ``auth:*``, 4 rôles système et le mapping rôle → permissions, déterministe et sans I/O.

## Critères d'acceptation

- Les 10 permissions système existent (``is_system=True``, resource/action/description).
- Les 4 rôles système existent (USER, ADMIN, SERVICE, SUPER_ADMIN).
- Mapping conforme : USER lecture seule, ADMIN large hors JWK rotate, SERVICE vide, SUPER_ADMIN = toutes ``auth:*``.
- Ordre déterministe, collections immuables, exporté depuis ``baobab_auth_core``.
