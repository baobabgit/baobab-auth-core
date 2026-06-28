"""Test d'architecture — ``src/`` ne dépend d'aucune infrastructure.

Garantit que le core reste une librairie métier pure : aucun import de framework
web, ORM, client HTTP, librairie crypto concrète, ni accès fichier/réseau/env var.

:spec: BL-040-011
"""

import re
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent.parent / "src" / "baobab_auth_core"

# Modules/usages d'infrastructure interdits dans le core de production.
_FORBIDDEN_PATTERNS = (
    r"\bimport\s+fastapi\b",
    r"\bfrom\s+fastapi\b",
    r"\bimport\s+sqlalchemy\b",
    r"\bfrom\s+sqlalchemy\b",
    r"\bimport\s+alembic\b",
    r"\bimport\s+psycopg\w*\b",
    r"\bimport\s+jwt\b",
    r"\bfrom\s+jwt\b",
    r"\bimport\s+jose\b",
    r"\bimport\s+argon2\b",
    r"\bimport\s+bcrypt\b",
    r"\bimport\s+httpx\b",
    r"\bimport\s+requests\b",
    r"\bimport\s+socket\b",
    r"\bos\.environ\b",
    r"\bos\.getenv\b",
    r"\bopen\s*\(",
)


def _python_files() -> list[Path]:
    return [p for p in _SRC.rglob("*.py")]


class TestNoInfrastructureDependencies:
    def test_BL_040_011_1_src_existe(self) -> None:
        assert _SRC.is_dir()
        assert _python_files()

    def test_BL_040_011_2_aucun_import_infrastructure(self) -> None:
        violations: list[str] = []
        compiled = [re.compile(p) for p in _FORBIDDEN_PATTERNS]
        for path in _python_files():
            content = path.read_text(encoding="utf-8")
            for pattern in compiled:
                if pattern.search(content):
                    violations.append(f"{path.name}: {pattern.pattern}")
        assert not violations, f"Dépendances interdites détectées : {violations}"
