# Cahier des charges — `baobab-auth-core` — Version `0.5.0`

**Projet :** `baobab-auth-core`  
**Type de document :** cahier des charges versionné  
**Destination :** IA de développement  
**Format :** Markdown  
**Règle d'architecture constante :** le core reste une librairie métier pure, sans FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT concret, Argon2, bcrypt, httpx, requests, Docker ou accès fichier/réseau/env var en production.

---


## 1. Objectif de la version

La version `0.5.0` stabilise les contrats publics et prépare l'intégration inter-briques. Elle ne doit pas ajouter d'infrastructure dans le core, mais rendre ses interfaces suffisamment stables pour `database`, `security`, `api`, `client` et `admin`.

Jalon :

```text
0.5.0 → Stabilisation des contrats publics et pré-intégration
```

---

## 2. Préconditions

```text
v0.3.0 RBAC validée
v0.4.0 catalogue/durcissement validé
DefaultAuthCatalog disponible
exceptions métier stables
DTO principaux disponibles
ports principaux disponibles
coverage ≥ 90 %
```

---

## 3. Périmètre inclus

```text
exports publics stabilisés
DTO applicatifs stabilisés
codes d'erreurs métier
contrat database
contrat security
contrat api
contrat client
contrat admin
cas d'usage de lecture
cas d'usage admin métier
tests contractuels inter-briques
documentation d'intégration
```

---

## 4. API publique

Le package racine doit exposer clairement :

```text
Entités: User, UserProfile, Role, Permission, Session, AuditEvent
Value objects: Email, AuthSubject, Password/PlainPassword, PasswordHash, RoleName, PermissionName, SessionId, TokenId
Enums: UserStatus, SessionStatus, AuditEventType, AuditSeverity
Policies: PasswordPolicy, SessionPolicy, RolePolicy, PermissionPolicy, LockoutPolicy
Catalogues: DefaultAuthCatalog
Ports: repositories, PasswordHasher, TokenProvider, Clock, IdGenerator, UnitOfWork
DTO: AuthContext, AuthenticatedUser, TokenPair, TokenClaims, SessionDTO
Use cases: RegisterUser, AuthenticateUser, RefreshSession, Logout, RevokeSession, RevokeAllSessions, AssignRole, RemoveRole, ChangePassword
```

Ajouter `__all__` cohérent et tests d'import.

---

## 5. DTO applicatifs

### 5.1 `AuthenticatedUser`

Sans secret. Champs :

```text
id
auth_subject
email
status
roles
permissions
```

### 5.2 `SessionDTO`

Sans refresh token brut ni hash.

### 5.3 `TokenPair`

Contient tokens retournables, mais `repr()` doit être sûr si possible.

### 5.4 `TokenClaims`

Doit représenter :

```text
sub/AuthSubject
sid/SessionId
jti/TokenId
roles
permissions
iat
exp
iss
aud
```

### 5.5 `TokenIssueContext`

Créer ou stabiliser pour `security` :

```text
subject
user_id
session_id
roles
permissions
issued_at
access_expires_at
refresh_expires_at
issuer
audience
```

---

## 6. Codes d'erreurs métier

Chaque exception publique doit fournir :

```text
error_code
safe_message
```

Exemples :

| Exception | error_code | HTTP recommandé |
|---|---|---:|
| InvalidCredentialsError | auth.credentials.invalid | 401 |
| ForbiddenError | auth.authorization.forbidden | 403 |
| PermissionDeniedError | auth.authorization.permission_denied | 403 |
| UserNotFoundError | auth.user.not_found | 404 |
| UserAlreadyExistsError | auth.user.already_exists | 409 |
| LastSuperAdminRoleRemovalError | auth.role.last_super_admin | 409 |
| UserLockedError | auth.user.locked | 423 |

---

## 7. Contrat database

Stabiliser :

```text
UserRepository
RoleRepository
PermissionRepository
SessionRepository
AuditRepository
UnitOfWork
```

Règles :

- entités mappables ;
- `DefaultAuthCatalog` utilisable pour seed ;
- aucune connaissance des noms de tables dans le core ;
- `AuditEvent.metadata` JSON-sérialisable ;
- dates UTC aware.

---

## 8. Contrat security

Stabiliser :

```text
PasswordHasher
TokenProvider
TokenIssueContext
TokenClaims
TokenPair
```

Règles :

- le core ne dépend pas de JWT concret ;
- le core ne dépend pas d'Argon2/bcrypt ;
- `sub` correspond à `AuthSubject` ;
- `jti` correspond à `TokenId` ;
- `sid` correspond à `SessionId`.

---

## 9. Contrat API

Préparer les cas d'usage nécessaires à :

```text
POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout
GET /auth/me
GET /auth/roles
GET /auth/permissions
GET /auth/sessions
POST /auth/sessions/{id}/revoke
POST /auth/users/{id}/roles
DELETE /auth/users/{id}/roles/{role}
POST /auth/users/{id}/disable
POST /auth/users/{id}/enable
POST /auth/jwks/rotation-request
```

Le core ne doit jamais retourner `HTTPException`.

---

## 10. Contrat client

Stabiliser :

```text
AuthSubject
AuthContext
AuthenticatedUser
TokenClaims
RoleName
PermissionName
```

Le client ne recalcule pas les permissions depuis les rôles.

---

## 11. Contrat admin

Préparer :

```text
BootstrapSuperAdmin
DisableUser
EnableUser
RequestJwkRotation
ListRoles
ListPermissions
ListUserSessions
```

---

## 12. Cas d'usage nouveaux ou à stabiliser

```text
GetUserBySubject
GetCurrentUser
ListRoles
ListPermissions
ListUserSessions
DisableUser
EnableUser
BootstrapSuperAdmin
RequestJwkRotation
```

Chacun doit avoir commande/query, résultat, règles métier, audit et tests.

---

## 13. Tests contractuels

Créer :

```text
tests/contracts/database/
tests/contracts/security/
tests/contracts/api/
tests/contracts/client/
tests/contracts/admin/
```

Ces tests ne doivent pas importer les autres briques.

---

## 14. Backlog détaillé

```text
BL-050-001 Stabiliser exports publics
BL-050-002 Stabiliser DTO applicatifs
BL-050-003 Ajouter codes d'erreurs métier
BL-050-004 Harmoniser ports repositories
BL-050-005 Stabiliser PasswordHasher
BL-050-006 Stabiliser TokenProvider
BL-050-007 Ajouter cas d'usage de lecture
BL-050-008 Ajouter cas d'usage admin métier
BL-050-009 Ajouter tests contractuels inter-briques
BL-050-010 Documenter contrats d'intégration
BL-050-011 Mettre à jour README et CHANGELOG
BL-050-012 Renforcer tests de pureté du core
```

---

## 15. Documentation

```text
docs/public_api.md
docs/error_codes.md
docs/database_contract.md
docs/security_contract.md
docs/api_contract.md
docs/client_contract.md
docs/admin_contract.md
docs/integration_contracts.md
docs/versioning.md
```

---

## 16. Critères de définition de terminé

`0.5.0` est terminée si :

- API publique documentée ;
- DTO sans secret ;
- exceptions avec `error_code` et `safe_message` ;
- contrats database/security/api/client/admin documentés ;
- cas d'usage de lecture disponibles ;
- cas admin disponibles ou report justifié ;
- tests contractuels présents ;
- aucune dépendance interdite ;
- `ruff`, `mypy`, `pytest` OK ;
- couverture ≥ 90 %.
