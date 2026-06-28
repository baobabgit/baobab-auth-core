# Revue — BL-030-006

## Verdict

**APPROUVÉ** — prêt pour merge vers `version/v0.3.0`.

## Points vérifiés

- Export public des exceptions RBAC (`AuthorizationError`, `ForbiddenError`,
  `PermissionDeniedError`, `RoleError`, `RoleNotFoundError`, `PermissionNotFoundError`,
  `LastSuperAdminRoleRemovalError`).
- Alias rétrocompatible `LastAdminRoleRemovalError`.
- Docstrings RST et contrats `public_api.md` / `imports.md` à jour.
- Qualité : black, ruff, mypy, bandit, couverture ≥ 95 %, build, traceability.
