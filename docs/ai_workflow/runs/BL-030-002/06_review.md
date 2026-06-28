# Review — BL-030-002

## Décision

TECH_REVIEW_PASSED

## Vérifications

- `AuthorizationService` charge l'utilisateur via `UserRepository`.
- Les rôles connus sont chargés via `RoleRepository` et les rôles inconnus sont
  ignorés conformément à l'ADR-0009.
- Les permissions associées aux rôles connus sont chargées via
  `PermissionRepository` puis dédupliquées par `AuthContext`.
- `has_role`, `has_permission`, `require_role` et `require_permission` couvrent
  les chemins nominaux et les refus métier.
- `ForbiddenError`, `PermissionDeniedError` et `UserNotFoundError` restent les
  exceptions stables utilisées sans introduire de dépendance technique.
- Tests miroir ajoutés et gates qualité complets passés.

## Risques résiduels

- Les permissions référencées par un rôle mais absentes du dépôt sont ignorées
  pendant l'agrégation ; ce comportement est couvert par test et reste aligné
  avec une construction de contexte tolérante en v0.3.0.
