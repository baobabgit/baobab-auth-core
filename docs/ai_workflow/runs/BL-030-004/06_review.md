# Review — BL-030-004

## Décision

TECH_REVIEW_PASSED

## Vérifications

- `AssignRoleCommand` accepte `AuthSubject | str`, `UserId | str` et
  `RoleName | str` conformément au cahier v0.3.0.
- `AssignRole` construit le contexte acteur via `AuthorizationService`.
- L'autorisation minimale v0.3.0 accepte `ADMIN` ou `SUPER_ADMIN`.
- La cible et le rôle sont validés via les ports dédiés.
- L'assignation est idempotente : une cible qui possède déjà le rôle ne produit
  ni doublon, ni audit supplémentaire.
- L'audit `ROLE_ASSIGNED` est produit avec sévérité `WARNING`, sans secret, et
  la sauvegarde cible + audit sont committés dans le même `UnitOfWork`.
- Tests miroir ajoutés et gates qualité complets passés.

## Risques résiduels

- Le contrôle fin par permission `auth:role:write` reste explicitement reporté
  à v0.4.0 par le cahier des charges.
