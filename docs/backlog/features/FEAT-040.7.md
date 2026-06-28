# FEAT-040.7 — Tests d'architecture anti-dépendances

| Champ | Valeur |
|-------|--------|
| Rattachée à | [US-040](../user_stories/US-040.md) |
| Statut | Implémentée ✅ |
| Spec dérivée | [`FEAT-040.7`](../../specifications/us/US-040-durcissement-rbac/) |

## Livrables

Test garantissant l'absence de dépendance d'infrastructure dans ``src/``.

## Critères d'acceptation

- Aucun import interdit (fastapi, sqlalchemy, jwt, argon2, bcrypt, httpx, requests, os.environ, open, socket) dans ``src/``.
