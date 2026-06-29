# Rapport d'intégration — baobab-auth-core v0.5.1 ↔ baobab-auth-database v0.1.0

**Date** : 2026-06-29  
**Producteur** : baobab-auth-core `0.5.1` (PyPI)  
**Consommateur** : baobab-auth-database `v0.1.0` / branche `version/v0.1.0`  
**Contrat** : `database`  
**Verdict** : **PASSED**

## Synthèse

``baobab-auth-database`` valide le contrat ``database`` du core v0.5.1.
Premier consommateur de la chaîne d'intégration v0.5.x (ordre 1/5).

Rapport miroir côté consommateur :
``baobab-auth-database/docs/integrations/reports/baobab-auth-core-v0.5.1__baobab-auth-database-v0.1.0.md``

## Fonctionnalités core validées par baobab-auth-database

### Ports de persistance (protocoles runtime)

| Port core | Implémentation database | Validé |
|-----------|-------------------------|--------|
| ``UserRepository`` | ``SqlAlchemyUserRepository`` | oui |
| ``RoleRepository`` | ``SqlAlchemyRoleRepository`` | oui |
| ``PermissionRepository`` | ``SqlAlchemyPermissionRepository`` | oui |
| ``SessionRepository`` | ``SqlAlchemySessionRepository`` | oui |
| ``AuditRepository`` | ``SqlAlchemyAuditRepository`` | oui |
| ``UnitOfWork`` | ``SqlAlchemyAuthUnitOfWork`` | oui |

### Catalogue et entités

| Fonctionnalité core | Usage database | Validé |
|---------------------|----------------|--------|
| ``DefaultAuthCatalog`` | ``AuthCatalogBootstrap`` (seed idempotent) | oui |
| Entités ``User``, ``Role``, ``Permission``, ``Session``, ``AuditEvent`` | Mappers ORM ↔ domaine | oui |
| Value objects (``Email``, ``AuthSubject``, ``RoleName``, etc.) | Repositories + mappers | oui |

### Comportements transactionnels

- ``UnitOfWork.__enter__`` / ``__exit__`` avec rollback sur exception
- ``commit()`` / ``rollback()`` explicites
- Session SQLAlchemy partagée entre repositories de l'UoW

### CLI opérationnelle (consommateur)

- Migrations Alembic embarquées (`upgrade`, `downgrade`, `current`, `history`)
- Bootstrap catalogue (`bootstrap`)

## Commandes de validation (côté database)

```bash
uv run pytest tests/contracts/ -v
uv run nox -s all
```

Résultat : 97 tests PASS, couverture 96,52 %, CI PR #12 verte.

## Consommateurs restants (core v0.5.x)

| Ordre | Consommateur | Statut |
|-------|--------------|--------|
| 1 | baobab-auth-database | **PASSED** |
| 2 | baobab-auth-security | PENDING |
| 3 | baobab-auth-api | PENDING |
| 4 | baobab-auth-client | PENDING |
| 5 | baobab-auth-admin | PENDING |

Le core n'atteint ``INTEGRATION_VALIDATED`` que lorsque les 5 consommateurs requis
ont ``status: PASSED``.
