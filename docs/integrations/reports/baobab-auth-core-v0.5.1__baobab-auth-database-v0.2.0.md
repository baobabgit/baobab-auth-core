# Rapport d'intégration — baobab-auth-core v0.5.1 × baobab-auth-database v0.2.0

Date : 2026-06-28  
Producteur : baobab-auth-core  
Consommateur : baobab-auth-database (git-ref `version/v0.2.0`)  
Résultat : **PASSED**

## Fonctionnalités core validées par database v0.2.0

| Domaine core | Usage database v0.2.0 |
|---|---|
| ``DefaultAuthCatalog`` | Seed, checksum, diagnostics |
| ``Permission`` / ``Role`` | Persistance et comparaison catalogue |
| ``RoleName`` / ``PermissionName`` | Mappings rôle → permissions |
| Ports repositories + UoW | Inchangés depuis v0.1.0 |

## Scénarios catalogue

- Checksum déterministe du catalogue installé.
- ``catalog check`` : exit 0 conforme / 1 divergent.
- ``catalog seed`` : idempotent + trace ``auth_catalog_versions``.
- Rôle ``SERVICE`` sans permission ; ``SUPER_ADMIN`` avec toutes les permissions core.

## Référence

Rapport producteur : `baobab-auth-database` —
`docs/integrations/reports/baobab-auth-core-v0.5.1__baobab-auth-database-v0.2.0.md`
