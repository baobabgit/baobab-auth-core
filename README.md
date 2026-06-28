# baobab-auth-core

[![CI](https://github.com/baobabgit/baobab-auth-core/actions/workflows/ci.yml/badge.svg)](https://github.com/baobabgit/baobab-auth-core/actions/workflows/ci.yml)
[![Integration](https://github.com/baobabgit/baobab-auth-core/actions/workflows/integration.yml/badge.svg)](https://github.com/baobabgit/baobab-auth-core/actions/workflows/integration.yml)
[![Release](https://github.com/baobabgit/baobab-auth-core/actions/workflows/release.yml/badge.svg)](https://github.com/baobabgit/baobab-auth-core/actions/workflows/release.yml)
[![Python versions](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

Socle métier d'authentification et d'autorisation pour Python 3.13+.
Librairie **pure**, sans dépendances techniques : pas de framework web, pas d'ORM,
pas de JWT concret, pas de hachage cryptographique. Elle expose le **domaine**, les
**ports** (protocoles) et des **fakes** pour les tests — le reste s'adapte.

## Table des matières

- [À propos](#à-propos)
- [Installation](#installation)
- [Usage](#usage)
- [Qualité](#qualité)
- [Tests](#tests)
- [Release](#release)
- [Intégration inter-librairies](#intégration-inter-librairies)
- [Contribuer](#contribuer)
- [Licence](#licence)

## À propos

`baobab-auth-core` fournit les **briques métier** réutilisables d'un système
d'authentification :

- **Value objects** : `Email`, `PlainPassword`, `PasswordHash`, `RoleName`,
  `PermissionName`, identifiants typés (`UserId`, `SessionId`, …)
- **Entités** : `User`, `Role`, `Permission`, `Session`, `AuditEvent`, `UserProfile`
- **Politiques métier** : `PasswordPolicy`, `SessionPolicy`, `RolePolicy`
- **Enums** : `UserStatus`, `SessionStatus`, `AuditEventType`, `AuditSeverity`
- **Exceptions** hiérarchisées par famille (validation, user, auth, session, rôle, autorisation)
- **Ports** (protocoles Python) : `Clock`, `IdGenerator`, `PasswordHasher`,
  `TokenProvider`, `UserRepository`, `RoleRepository`, `PermissionRepository`,
  `SessionRepository`, `AuditRepository`, `UnitOfWork`
- **Fakes** testables : implémentations en mémoire de tous les ports, prêtes à l'emploi
  dans les suites de tests des projets consommateurs

## Installation

```bash
# Via pip
pip install baobab-auth-core

# Via uv (recommandé)
uv add baobab-auth-core
```

Prérequis : Python ≥ 3.13. Aucune dépendance de production.

## Usage

### Value objects

```python
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.exceptions.validation import InvalidEmailError

# Normalisation automatique (lowercase, uppercase)
email = Email("Alice@Example.COM")  # stocke "alice@example.com"
role = RoleName("admin")            # stocke "ADMIN"

# Protection contre les fuites dans les logs
password = PlainPassword("s3cr3t!")
print(password)   # "***"

try:
    bad = Email("not-an-email")
except InvalidEmailError:
    pass
```

### Entités avec comportement métier

```python
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.user_status import UserStatus

user = User(
    id=user_id,
    email=email,
    password_hash=hashed,
    status=UserStatus.PENDING,
    roles=[],
    failed_login_count=0,
    created_at=now,
    updated_at=now,
)

user.activate()
user.assign_role(role_name)
user.mark_login_failure()
```

### Politiques métier injectées

```python
from baobab_auth_core.domain.policies.password_policy import PasswordPolicy
from baobab_auth_core.exceptions.validation import WeakPasswordError

policy = PasswordPolicy(min_length=16, require_digit_or_symbol=True)
try:
    policy.validate(plain_password, email=user.email)
except WeakPasswordError as exc:
    print(exc.message)
```

### Fakes pour les tests

```python
from baobab_auth_core.testing.fake_clock import FakeClock
from baobab_auth_core.testing.fake_password_hasher import FakePasswordHasher
from baobab_auth_core.testing.in_memory_user_repository import InMemoryUserRepository

clock = FakeClock()
clock.advance(seconds=3600)  # avancer dans le temps

hasher = FakePasswordHasher()
hashed = hasher.hash(plain_password)       # "hashed:s3cr3t!"
assert hasher.verify(plain_password, hashed)

repo = InMemoryUserRepository()
await repo.save(user)
found = await repo.get_by_email(email)
```

### Autorisation RBAC (v0.3.0)

```python
from baobab_auth_core.application.results import AuthContext
from baobab_auth_core.application.services import AuthorizationService
from baobab_auth_core.application.commands.assign_role_command import AssignRoleCommand
from baobab_auth_core.application.use_cases.assign_role import AssignRole
from baobab_auth_core.exceptions import ForbiddenError, PermissionDeniedError

authorization = AuthorizationService(users, roles, permissions)
context: AuthContext = authorization.build_context("subject-alice")

authorization.require_permission(context, "auth:user:read")

assign = AssignRole(users, roles, authorization, audit, ids, clock, uow)
assign.execute(
    AssignRoleCommand(
        actor_subject="subject-admin",
        target_user_id="user-target",
        role_name="support",
    )
)
```

Voir le guide détaillé : [`docs/guides/rbac.rst`](docs/guides/rbac.rst).

## Qualité

Toutes les vérifications s'exécutent via `make all` (ou `uv run nox -s all`) :

```bash
# Séparément
uv run black --check src tests   # format
uv run ruff check src tests      # lint
uv run mypy src                  # typage strict
uv run bandit -r src -c pyproject.toml  # SAST

# Tout d'un coup
make all
```

Standards imposés : `black` (PEP 8, line-length 88), `ruff` (ANN + D + B + UP),
`mypy` strict, `bandit` (0 Medium/High).

## Tests

```bash
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=95
```

Couverture ≥ 95 % imposée par CI. Les tests d'intégration inter-librairies se trouvent
dans `tests/integration/`, les tests de contrat dans `tests/contracts/`.

## Release

Les releases suivent **SemVer**. Un tag `vX.Y.Z` sur `main` déclenche `release.yml`
(publication PyPI via Trusted Publishing OIDC). Voir `CHANGELOG.md` pour l'historique.

Rupture de l'API publique (suppression/modification d'un symbole dans `__all__`) →
bump **majeur** + entrée « BREAKING » dans `CHANGELOG.md`.

## Intégration inter-librairies

Les contrats publics sont dans [`docs/contracts/`](docs/contracts/).
La matrice de compatibilité est dans
[`docs/integrations/compatibility_matrix.yaml`](docs/integrations/compatibility_matrix.yaml).
Le workflow `integration.yml` valide automatiquement les intégrations déclarées.

## Contribuer

Les règles de développement vivent dans [`AGENTS.md`](AGENTS.md).
En résumé : branche `bl/XXX-description` depuis `version/vX.Y.Z`,
commit `BL-XXX: action courte`, PR verte (qualité + tests ≥ 95 % + build).

## Licence

Distribué sous licence **MIT**. Voir [`LICENSE`](LICENSE).
