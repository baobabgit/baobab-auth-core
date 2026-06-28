# Cahier des charges — `baobab-auth-core` — Version `0.1.0`

**Projet :** `baobab-auth-core`  
**Type de document :** cahier des charges versionné  
**Destination :** IA de développement  
**Format :** Markdown  
**Règle d'architecture constante :** le core reste une librairie métier pure, sans FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT concret, Argon2, bcrypt, httpx, requests, Docker ou accès fichier/réseau/env var en production.

---


## 1. Objectif de la version

La version `0.1.0` pose le socle métier minimal de `baobab-auth-core`. Elle doit fournir les objets du domaine, les value objects, les policies de base, les exceptions, les ports principaux et les fakes nécessaires aux tests. Elle ne doit pas encore fournir un parcours complet d'authentification avec sessions et tokens.

Cette version doit rendre possible le développement des versions suivantes sans réécrire le domaine.

## 2. Périmètre fonctionnel

La version doit couvrir :

- l'initialisation du package Python ;
- les entités métier principales ;
- les value objects métier ;
- les statuts et énumérations ;
- les politiques de mot de passe et de session ;
- les exceptions métier ;
- les ports principaux ;
- les fakes in-memory ;
- une documentation minimale ;
- une suite de tests unitaires.

## 3. Architecture cible

Arborescence recommandée :

```text
src/baobab_auth_core/
├── __init__.py
├── py.typed
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── enums/
│   ├── policies/
│   └── services/
├── application/
│   ├── commands/
│   ├── results/
│   └── use_cases/
├── ports/
├── exceptions/
└── testing/
```

Règles :

- le domaine ne dépend pas de `application` ;
- `application` dépend du domaine et des ports ;
- les ports ne dépendent d'aucune implémentation ;
- les fakes restent dans `testing` ;
- aucun code de production ne doit dépendre d'une brique technique.

## 4. Entités à implémenter

### 4.1 `User`

Champs minimaux :

```python
id: UserId | str
auth_subject: AuthSubject
email: Email
password_hash: PasswordHash
status: UserStatus
role_names: tuple[RoleName, ...]
created_at: datetime
updated_at: datetime
last_login_at: datetime | None
failed_login_count: int
locked_until: datetime | None
```

Méthodes attendues :

```python
activate(now)
disable(now)
lock(until, now)
unlock(now)
mark_login_success(now)
mark_login_failure(now)
change_password_hash(password_hash, now)
assign_role(role_name, now)
remove_role(role_name, now)
has_role(role_name)
```

Invariants :

- `email` obligatoire et normalisé ;
- `auth_subject` obligatoire et stable ;
- `password_hash` jamais vide ;
- `failed_login_count >= 0` ;
- dates UTC aware ;
- rôles sans doublon.

### 4.2 `UserProfile`

Champs :

```python
user_id: UserId | str
display_name: str | None
locale: str | None
timezone: str | None
avatar_url: str | None
created_at: datetime
updated_at: datetime
```

Aucun secret ne doit être présent.

### 4.3 `Role`

Champs :

```python
id: RoleId | str
name: RoleName
description: str | None
permission_names: tuple[PermissionName, ...]
is_system: bool
created_at: datetime
updated_at: datetime
```

### 4.4 `Permission`

Champs :

```python
id: PermissionId | str
name: PermissionName
resource: str
action: str
description: str | None
is_system: bool
```

### 4.5 `Session`

Champs :

```python
id: SessionId | str
user_id: UserId | str
refresh_token_id: TokenId
status: SessionStatus
created_at: datetime
expires_at: datetime
revoked_at: datetime | None
last_used_at: datetime | None
user_agent: str | None
ip_address: str | None
device_label: str | None
```

### 4.6 `AuditEvent`

Champs :

```python
id: AuditEventId | str
event_type: AuditEventType
actor_subject: AuthSubject | None
target_type: str | None
target_id: str | None
ip_address: str | None
user_agent: str | None
metadata: Mapping[str, Any]
severity: AuditSeverity
created_at: datetime
```

## 5. Value objects à implémenter

Créer au minimum :

```text
Email
AuthSubject
PlainPassword ou Password
PasswordHash
RoleName
PermissionName
UserId
RoleId
PermissionId
SessionId
TokenId
AuditEventId
```

Règles importantes :

- `Email` normalise en minuscules ;
- `RoleName` refuse vide et espaces ;
- `PermissionName` valide le format `scope:resource:action` ;
- `PlainPassword` et `PasswordHash` masquent leur valeur dans `repr()` et `str()` ;
- les identifiants refusent une valeur vide.

## 6. Énumérations

Créer :

```text
UserStatus: PENDING, ACTIVE, LOCKED, DISABLED, DELETED
SessionStatus: ACTIVE, REVOKED, EXPIRED
AuditSeverity: INFO, WARNING, CRITICAL
AuditEventType: USER_REGISTERED, LOGIN_SUCCESS, LOGIN_FAILURE, LOGOUT, SESSION_REFRESHED, SESSION_REVOKED, ROLE_ASSIGNED, ROLE_REMOVED, PASSWORD_CHANGED, ACCOUNT_LOCKED, ACCOUNT_DISABLED, ACCOUNT_DELETED
```

Les événements pourront être enrichis dans les versions suivantes.

## 7. Policies

### 7.1 `PasswordPolicy`

Règles par défaut :

```text
min_length = 12
max_length = 256
require_letter = True
require_digit_or_symbol = True
forbid_email_as_password = True
```

### 7.2 `SessionPolicy`

Règles par défaut :

```text
access_token_ttl_seconds = 900
refresh_token_ttl_seconds = 2592000
max_failed_login_attempts = 5
lockout_duration_seconds = 900
revoke_other_sessions_on_password_change = True
```

### 7.3 `RolePolicy`

Règles initiales :

```text
default_role_name = USER
super_admin_role_name = SUPER_ADMIN
enforce_last_super_admin = True
```

## 8. Ports à définir

Créer des protocoles :

```text
UserRepository
RoleRepository
PermissionRepository
SessionRepository
AuditRepository
PasswordHasher
TokenProvider
Clock
IdGenerator
UnitOfWork
```

Les signatures peuvent être synchrones ou asynchrones selon l'état du projet, mais doivent être homogènes et documentées.

## 9. Exceptions à créer

Hiérarchie minimale :

```text
BaobabAuthCoreError
ValidationError
InvalidEmailError
WeakPasswordError
InvalidRoleNameError
InvalidPermissionNameError
UserAlreadyExistsError
UserNotFoundError
UserDisabledError
UserLockedError
UserDeletedError
InvalidCredentialsError
TokenInvalidError
TokenExpiredError
SessionNotFoundError
SessionExpiredError
SessionRevokedError
AuthorizationError
ForbiddenError
PermissionDeniedError
RoleNotFoundError
PermissionNotFoundError
LastSuperAdminRoleRemovalError
```

Les messages ne doivent contenir aucun secret.

## 10. Fakes de test

Fournir :

```text
FakeClock
FakeIdGenerator
FakePasswordHasher
FakeTokenProvider
InMemoryUserRepository
InMemoryRoleRepository
InMemoryPermissionRepository
InMemorySessionRepository
InMemoryAuditRepository
InMemoryUnitOfWork
```

## 11. Tests obligatoires

Créer des tests pour :

- chaque value object ;
- chaque entité ;
- chaque policy ;
- chaque fake ;
- hiérarchie d'exceptions ;
- absence de secret dans `repr()` ;
- absence de dépendances techniques interdites.

Objectif de couverture :

```text
coverage >= 85 % pour 0.1.0
coverage cible >= 90 % dès 0.2.0
```

## 12. Documentation attendue

Créer :

```text
README.md
CHANGELOG.md
docs/domain_model.md
docs/ports.md
docs/testing.md
```

## 13. Backlog détaillé

### BL-010-001 — Initialiser le package

Créer structure `src/`, `pyproject.toml`, `README.md`, `CHANGELOG.md`, `py.typed`.

### BL-010-002 — Implémenter value objects

Créer les value objects et tests.

### BL-010-003 — Implémenter entités

Créer entités et méthodes métier.

### BL-010-004 — Implémenter enums et policies

Créer statuts, événements et policies.

### BL-010-005 — Implémenter exceptions

Créer hiérarchie métier.

### BL-010-006 — Définir ports

Créer protocoles et documentation.

### BL-010-007 — Implémenter fakes

Créer fakes in-memory.

### BL-010-008 — Ajouter tests et documentation

Finaliser qualité minimale.

## 14. Critères de définition de terminé

La version `0.1.0` est terminée si :

- le package s'installe ;
- le domaine est importable ;
- les entités principales existent ;
- les value objects principaux existent ;
- les policies existent ;
- les ports existent ;
- les fakes existent ;
- aucun import technique interdit n'est présent ;
- `ruff`, `mypy` et `pytest` passent ;
- la documentation minimale est disponible.
