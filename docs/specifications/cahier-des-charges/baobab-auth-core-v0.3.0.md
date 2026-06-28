# Cahier des charges — `baobab-auth-core` — Version `0.3.0`

**Projet :** `baobab-auth-core`  
**Type de document :** cahier des charges versionné  
**Destination :** IA de développement  
**Format :** Markdown  
**Règle d'architecture constante :** le core reste une librairie métier pure, sans FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT concret, Argon2, bcrypt, httpx, requests, Docker ou accès fichier/réseau/env var en production.

---


## 1. Objectif de la version

La version `0.3.0` stabilise le socle RBAC et l'autorisation métier.

Elle doit permettre :

- de définir des rôles ;
- de définir des permissions ;
- d'associer des permissions à des rôles ;
- d'associer des rôles à des utilisateurs ;
- de construire un `AuthContext` ;
- d'évaluer des rôles et permissions ;
- d'assigner un rôle ;
- de retirer un rôle ;
- d'auditer les modifications RBAC ;
- de tester le RBAC sans base de données ni API HTTP.

---

## 2. Préconditions

Les versions `0.1.0` et `0.2.0` doivent être validées.

Doivent déjà exister :

```text
User
Role
Permission
AuditEvent
RoleName
PermissionName
UserRepository
RoleRepository
PermissionRepository
AuditRepository
UnitOfWork
```

---

## 3. Périmètre inclus

```text
AuthContext
AuthorizationService
AssignRole
RemoveRole
RolePolicy renforcée
PermissionPolicy
Exceptions RBAC
Audit ROLE_ASSIGNED / ROLE_REMOVED
Fakes RBAC
Tests RBAC
Documentation RBAC
```

---

## 4. Entités et value objects RBAC

### 4.1 `Role`

Doit contenir :

```python
id: RoleId | str
name: RoleName
description: str | None
permission_names: tuple[PermissionName, ...]
is_system: bool
created_at: datetime
updated_at: datetime
```

### 4.2 `Permission`

Doit contenir :

```python
id: PermissionId | str
name: PermissionName
resource: str
action: str
description: str | None
is_system: bool
```

### 4.3 `RoleName`

Règles :

- refuse vide ;
- strip ;
- interdit espaces ;
- normalise les rôles système en majuscules ;
- hashable.

### 4.4 `PermissionName`

Règles :

- refuse vide ;
- strip ;
- normalise en minuscules ;
- format `scope:resource:action` ;
- segments non vides ;
- hashable.

---

## 5. `AuthContext`

### 5.1 Structure

```python
@dataclass(frozen=True)
class AuthContext:
    auth_subject: AuthSubject
    user_id: UserId | str | None
    session_id: SessionId | None
    roles: tuple[RoleName, ...]
    permissions: tuple[PermissionName, ...]
    authenticated_at: datetime | None
```

### 5.2 Méthodes

```python
has_role(role)
has_any_role(roles)
has_permission(permission)
has_any_permission(permissions)
has_all_permissions(permissions)
```

### 5.3 Invariants

- immutable ;
- aucun secret ;
- rôles dédupliqués ;
- permissions dédupliquées ;
- compatible avec l'API et le client.

---

## 6. `AuthorizationService`

### 6.1 Responsabilités

- charger un utilisateur ;
- lire ses rôles ;
- charger les rôles ;
- agréger les permissions ;
- construire `AuthContext` ;
- vérifier rôles et permissions ;
- lever des exceptions métier.

### 6.2 Interface

```python
build_context(auth_subject) -> AuthContext
has_role(context, role) -> bool
has_permission(context, permission) -> bool
require_role(context, role) -> None
require_permission(context, permission) -> None
```

### 6.3 Règle sur rôles inconnus

La stratégie doit être explicite :

```text
Option recommandée 0.3.0 : ignorer les rôles inconnus et documenter.
Option stricte possible : lever RoleNotFoundError.
```

Le choix doit être testé.

---

## 7. Ports RBAC

### 7.1 `RoleRepository`

```python
get_by_name(name: RoleName) -> Role | None
list_roles() -> tuple[Role, ...]
save(role: Role) -> None
count_users_with_role(name: RoleName) -> int  # optionnel en 0.3, requis plus tard
```

### 7.2 `PermissionRepository`

```python
get_by_name(name: PermissionName) -> Permission | None
list_permissions() -> tuple[Permission, ...]
save(permission: Permission) -> None
```

---

## 8. Cas d'usage `AssignRole`

### 8.1 Commande

```python
@dataclass(frozen=True)
class AssignRoleCommand:
    actor_subject: AuthSubject | str
    target_user_id: UserId | str
    role_name: RoleName | str
    ip_address: str | None = None
    user_agent: str | None = None
```

### 8.2 Règles

- acteur existant ;
- acteur `ADMIN` ou `SUPER_ADMIN` en `0.3.0` ;
- cible existante ;
- rôle existant ;
- assignation idempotente ;
- audit `ROLE_ASSIGNED` ;
- transaction atomique.

Le contrôle fin par permission `auth:role:write` sera durci en `0.4.0`.

---

## 9. Cas d'usage `RemoveRole`

### 9.1 Commande

```python
@dataclass(frozen=True)
class RemoveRoleCommand:
    actor_subject: AuthSubject | str
    target_user_id: UserId | str
    role_name: RoleName | str
    ip_address: str | None = None
    user_agent: str | None = None
```

### 9.2 Règles

- acteur existant ;
- acteur `ADMIN` ou `SUPER_ADMIN` en `0.3.0` ;
- cible existante ;
- retrait idempotent si rôle absent ;
- dernier `SUPER_ADMIN` protégé ;
- audit `ROLE_REMOVED` ;
- transaction atomique.

---

## 10. Exceptions RBAC

Doivent exister :

```text
AuthorizationError
ForbiddenError
PermissionDeniedError
RoleError
RoleNotFoundError
PermissionNotFoundError
LastSuperAdminRoleRemovalError
```

Si `LastAdminRoleRemovalError` existe, fournir alias rétrocompatible vers `LastSuperAdminRoleRemovalError`.

---

## 11. Audit RBAC

Événements obligatoires :

```text
ROLE_ASSIGNED → WARNING
ROLE_REMOVED  → WARNING
```

Métadonnées autorisées :

```python
{"role": "ADMIN", "target_user_id": "..."}
```

Interdit : password, token, secret, hash.

---

## 12. Tests obligatoires

Créer ou compléter :

```text
tests/application/services/test_authorization_service.py
tests/application/results/test_auth_context.py
tests/application/use_cases/test_assign_role.py
tests/application/use_cases/test_remove_role.py
tests/application/use_cases/test_rbac_audit.py
tests/domain/policies/test_role_policy.py
tests/domain/policies/test_permission_policy.py
tests/testing/test_in_memory_role_repository.py
tests/testing/test_in_memory_permission_repository.py
```

Cas :

- agrégation permissions multi-rôles ;
- permissions dédupliquées ;
- `require_role` OK/refus ;
- `require_permission` OK/refus ;
- assignation nominale ;
- assignation idempotente ;
- retrait nominal ;
- retrait idempotent ;
- dernier `SUPER_ADMIN` protégé ;
- audit sans secret.

---

## 13. Backlog détaillé

### BL-030-001 — Stabiliser `AuthContext`

### BL-030-002 — Implémenter `AuthorizationService`

### BL-030-003 — Finaliser ports RBAC

### BL-030-004 — Stabiliser `AssignRole`

### BL-030-005 — Stabiliser `RemoveRole`

### BL-030-006 — Stabiliser exceptions RBAC

### BL-030-007 — Compléter tests RBAC

### BL-030-008 — Documenter RBAC

---

## 14. Documentation attendue

```text
docs/rbac.md
docs/authorization.md
docs/roles_permissions.md
README.md
CHANGELOG.md
```

---

## 15. Critères de définition de terminé

La version `0.3.0` est terminée si :

- `AuthContext` est complet ;
- `AuthorizationService` agrège les permissions ;
- `AssignRole` fonctionne ;
- `RemoveRole` fonctionne ;
- dernier `SUPER_ADMIN` protégé ;
- audit RBAC produit ;
- exceptions RBAC stables ;
- fakes RBAC disponibles ;
- aucun import technique interdit ;
- `ruff`, `mypy`, `pytest` passent ;
- couverture ≥ 90 %.
