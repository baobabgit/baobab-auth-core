# Recovery — BL-030-006

## Contexte

Verrou orphelin détecté : `active_tool: codex`, `expires_at: 2026-06-28T13:29:30Z`
expiré à la reprise (2026-06-28T13:34:28Z).

## Diagnostic

- Branche active : `bl/030-006-stabilize-rbac-exceptions`
- Fichiers modifiés : exceptions RBAC (`role.py`, `__init__.py`), tests, contrats.
- `uv run nox -s all` : **PASSED** après correction tri imports ruff.

## Décision

Reprise sur BL-030-006 (implémentation terminée, étape merge en cours).
