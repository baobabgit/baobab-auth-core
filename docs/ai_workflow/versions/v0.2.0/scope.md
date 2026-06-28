# Périmètre — v0.2.0

## Objectif

Ajouter le parcours d'authentification et de gestion de session au socle `0.1.0` :
inscription, authentification, création/rafraîchissement/révocation de session,
émission d'une paire de tokens via le port `TokenProvider`, audit et lockout minimal.
Le core reste une librairie métier pure (aucun JWT/Argon2 concret).

## Backlogs inclus

| ID | Titre | Priorité |
|----|-------|----------|
| BL-020-001 | Implémenter `RegisterUser` | P0 |
| BL-020-002 | Implémenter `AuthenticateUser` | P0 |
| BL-020-003 | Implémenter lockout minimal | P0 |
| BL-020-004 | Implémenter `RefreshSession` | P1 |
| BL-020-005 | Implémenter `Logout` | P1 |
| BL-020-006 | Implémenter `RevokeSession` | P1 |
| BL-020-007 | Stabiliser DTO tokens/session | P1 |
| BL-020-008 | Ajouter audit auth/session | P1 |
| BL-020-009 | Ajouter tests et documentation | P1 |

## Décisions d'architecture

- **ADR-0007** : extension du port `TokenProvider` (refresh tokens + révocation).
- **ADR-0008** : report de `AuthContext` complet à v0.3.0 ; `RevokeSession` accepte
  un acteur minimal en v0.2.0.

## Backlogs reportés

- Contrôle d'autorisation fin par permission (`auth:role:write`, `AuthContext` complet) → v0.3.0.
