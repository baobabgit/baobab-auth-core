# Tests Report — BL-030-002

## Résultat

Status : PASSED

## Commandes exécutées

- `uv run pytest tests/unit/baobab_auth_core/application/services/test_authorization_service.py --no-cov`
- `uv run black --check src tests`
- `uv run ruff check src tests`
- `uv run mypy src`
- `uv run bandit -r src -c pyproject.toml`
- `uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=95`
- `uv run python scripts/check_traceability.py`
- `uv build`
- `uv run twine check dist/*`

## Couverture

317 tests passés. Couverture totale : 99.42 %.
