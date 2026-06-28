# Périmètre — v0.3.0

## Objectif

Stabiliser le socle RBAC et l'autorisation métier sans introduire de dépendance
technique en production. La version couvre la construction d'un `AuthContext`,
l'agrégation des permissions par rôle, les cas d'usage d'assignation et retrait
de rôle, l'audit RBAC, les fakes de test et la documentation d'intégration.

## Backlogs inclus

| ID | Titre | Priorité |
|----|-------|----------|
| BL-030-001 | Stabiliser `AuthContext` | P0 |
| BL-030-002 | Implémenter `AuthorizationService` | P0 |
| BL-030-003 | Finaliser ports, policies et fakes RBAC | P0 |
| BL-030-004 | Stabiliser `AssignRole` | P0 |
| BL-030-005 | Stabiliser `RemoveRole` | P0 |
| BL-030-006 | Stabiliser exceptions RBAC | P1 |
| BL-030-007 | Compléter audit et tests RBAC | P1 |
| BL-030-008 | Documenter RBAC | P1 |

## Décisions d'architecture

- **ADR-0009** : RBAC applicatif pur, `AuthContext` immutable, rôles inconnus ignorés.

## Backlogs reportés

- Contrôle fin par permission `auth:role:write` durci en v0.4.0.
