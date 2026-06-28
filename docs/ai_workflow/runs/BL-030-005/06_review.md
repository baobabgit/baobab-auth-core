# Review — BL-030-005

## Décision

TECH_REVIEW_PASSED

## Vérifications

- `RemoveRoleCommand` accepte `AuthSubject | str`, `UserId | str` et
  `RoleName | str` conformément au cahier v0.3.0.
- `RemoveRole` construit le contexte acteur via `AuthorizationService`.
- L'autorisation minimale v0.3.0 accepte `ADMIN` ou `SUPER_ADMIN`.
- La cible et le rôle sont validés via les ports dédiés.
- Le retrait est idempotent si la cible ne possède pas le rôle.
- `RolePolicy.can_remove_role` protège le dernier `SUPER_ADMIN`.
- L'audit `ROLE_REMOVED` est produit avec sévérité `WARNING`, sans secret, et
  la sauvegarde cible + audit sont committés dans le même `UnitOfWork`.
- Tests miroir ajoutés et gates qualité complets passés.

## Risques résiduels

- Le comptage `count_users_with_role` doit être exact dans les implémentations
  persistantes pour préserver l'invariant du dernier `SUPER_ADMIN`.
