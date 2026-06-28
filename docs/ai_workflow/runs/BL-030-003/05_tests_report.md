# Tests Report — BL-030-003

## Résultat

Status : PASSED

## Commandes exécutées

- `uv run pytest tests/unit/baobab_auth_core/domain/policies/test_permission_policy.py tests/unit/baobab_auth_core/domain/policies/test_role_policy.py tests/unit/baobab_auth_core/domain/value_objects/test_permission_name.py tests/unit/baobab_auth_core/testing/test_in_memory_role_repository.py tests/unit/baobab_auth_core/testing/test_in_memory_permission_repository.py tests/unit/baobab_auth_core/ports/test_ports_protocol.py --no-cov`
- `uv run black --check src tests`
- `uv run ruff check src tests`
- `uv run mypy src`
- `uv run bandit -r src -c pyproject.toml`
- `uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=95`
- `uv run python scripts/check_traceability.py`
- `uv build`
- `uv run twine check dist/*`

## Couverture

311 tests passés. Couverture totale : 99.25 %.
