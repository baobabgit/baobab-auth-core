# Cahier des charges — `baobab-auth-core` — Version `0.4.0`

**Projet :** `baobab-auth-core`  
**Type de document :** cahier des charges versionné  
**Destination :** IA de développement  
**Format :** Markdown  
**Règle d'architecture constante :** le core reste une librairie métier pure, sans FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT concret, Argon2, bcrypt, httpx, requests, Docker ou accès fichier/réseau/env var en production.

---


## 1. Objectif de la version

La version `0.4.0` transforme le RBAC fonctionnel de `0.3.0` en un socle contractuel durci. Elle doit finaliser le catalogue système, le mapping rôle → permissions, les règles strictes `SUPER_ADMIN`, l'audit de sécurité et les tests d'architecture.

Jalon :

```text
0.4.0 → Durcissement sécurité + conformité contractuelle RBAC
```

---

## 2. Préconditions

Doivent être fonctionnels :

```text
AuthContext
AuthorizationService
AssignRole
RemoveRole
Role
Permission
RoleName
PermissionName
AuditEvent
RevokeAllSessions
ChangePassword
LockoutPolicy
fakes in-memory
coverage ≥ 90 %
```

---

## 3. Périmètre inclus

```text
DefaultAuthCatalog
4 rôles système
10 permissions auth:*
mapping rôle → permissions
règles strictes SUPER_ADMIN
exception LastSuperAdminRoleRemovalError
audit JWK_ROTATION_REQUESTED
sécurisation metadata audit
tests anti-dépendances
README / docs RBAC / security_rules / audit / integration_contracts
```

---

## 4. `DefaultAuthCatalog`

### 4.1 Emplacement

```text
src/baobab_auth_core/domain/catalogs/default_auth_catalog.py
src/baobab_auth_core/domain/catalogs/__init__.py
```

Exporter depuis :

```text
baobab_auth_core.__init__
```

### 4.2 Interface

```python
class DefaultAuthCatalog:
    def permissions(self) -> tuple[Permission, ...]: ...
    def roles(self) -> tuple[Role, ...]: ...
    def role_permissions(self) -> Mapping[RoleName, tuple[PermissionName, ...]]: ...
```

### 4.3 Règles

- ordre déterministe ;
- aucune base de données ;
- aucune variable d'environnement ;
- aucune permission applicative codée en dur ;
- collections immuables ou traitées comme telles.

---

## 5. Permissions système obligatoires

Le catalogue doit contenir exactement :

```text
auth:user:read
auth:user:write
auth:user:disable
auth:role:read
auth:role:write
auth:session:read
auth:session:revoke
auth:audit:read
auth:jwk:read
auth:jwk:rotate
```

Chaque permission doit avoir :

```text
name
resource
action
description
is_system=True
```

---

## 6. Rôles système obligatoires

```text
USER
ADMIN
SERVICE
SUPER_ADMIN
```

Règles :

- `USER` est le rôle par défaut ;
- `ADMIN` administre sans rotation de clé ni gestion critique `SUPER_ADMIN` ;
- `SERVICE` n'a aucune permission par défaut ;
- `SUPER_ADMIN` possède toutes les permissions `auth:*`.

---

## 7. Mapping rôle → permissions

| Rôle | Permissions |
|---|---|
| `USER` | `auth:user:read`, `auth:session:read` |
| `ADMIN` | `auth:user:read`, `auth:user:write`, `auth:user:disable`, `auth:role:read`, `auth:session:read`, `auth:session:revoke`, `auth:audit:read`, `auth:jwk:read` |
| `SERVICE` | aucune |
| `SUPER_ADMIN` | toutes les permissions `auth:*` |

Règle d'ownership : `USER` lit uniquement sa propre identité et ses propres sessions.

---

## 8. Règles strictes `SUPER_ADMIN`

Un acteur `ADMIN` ne peut pas :

```text
attribuer SUPER_ADMIN
retirer SUPER_ADMIN
retirer le dernier SUPER_ADMIN
déclencher une demande de rotation JWK
modifier les permissions système critiques
```

`AssignRole` doit refuser l'attribution de `SUPER_ADMIN` si l'acteur n'est pas `SUPER_ADMIN`.

`RemoveRole` doit refuser le retrait de `SUPER_ADMIN` si l'acteur n'est pas `SUPER_ADMIN`, puis vérifier la protection du dernier `SUPER_ADMIN`.

---

## 9. `RolePolicy`

Compléter :

```python
is_super_admin_role(role) -> bool
can_assign_role(actor_roles, role) -> bool
can_remove_role(actor_roles, role) -> bool
```

---

## 10. Exceptions

Créer ou stabiliser :

```text
LastSuperAdminRoleRemovalError
```

Conserver alias rétrocompatible si nécessaire :

```text
LastAdminRoleRemovalError
```

---

## 11. Audit

Ajouter :

```text
JWK_ROTATION_REQUESTED → CRITICAL
```

Vérifier :

```text
ROLE_ASSIGNED → WARNING
ROLE_REMOVED → WARNING
PASSWORD_CHANGED → WARNING
ACCOUNT_LOCKED → WARNING
```

Les métadonnées d'audit ne doivent jamais contenir :

```text
password
plain_password
password_hash
access_token
refresh_token
private_key
secret
cookie
authorization
```

---

## 12. Durcissements applicatifs

### 12.1 `ChangePassword`

Règles :

- ancien mot de passe vérifié ;
- nouveau mot de passe validé ;
- nouveau différent de l'ancien ;
- hash via port ;
- révocation autres sessions selon policy ;
- audit sans secret.

### 12.2 `RevokeAllSessions`

Règles :

- utilisateur peut révoquer ses sessions ;
- admin peut révoquer sessions standard ;
- politique spéciale pour éviter neutralisation abusive d'un `SUPER_ADMIN` ;
- audit `ALL_SESSIONS_REVOKED` avec count.

### 12.3 `AuthenticateUser`

Règles :

- erreur générique ;
- lockout après N échecs ;
- audit `LOGIN_FAILURE` et `ACCOUNT_LOCKED` ;
- succès réinitialise compteur.

---

## 13. Tests obligatoires

```text
tests/domain/catalogs/test_default_auth_catalog_permissions.py
tests/domain/catalogs/test_default_auth_catalog_roles.py
tests/domain/catalogs/test_default_auth_catalog_mapping.py
tests/domain/policies/test_role_policy_super_admin.py
tests/application/use_cases/test_super_admin_guards.py
tests/domain/enums/test_audit_event_type.py
tests/domain/entities/test_audit_event_safety.py
tests/application/use_cases/test_change_password_hardening.py
tests/application/use_cases/test_revoke_all_sessions_hardening.py
tests/application/use_cases/test_authenticate_user_lockout.py
tests/architecture/test_no_infrastructure_dependencies.py
```

---

## 14. Backlog détaillé

```text
BL-040-001 Créer DefaultAuthCatalog
BL-040-002 Implémenter 10 permissions système
BL-040-003 Implémenter 4 rôles système
BL-040-004 Implémenter mapping rôle → permissions
BL-040-005 Renforcer AssignRole pour SUPER_ADMIN
BL-040-006 Renforcer RemoveRole pour SUPER_ADMIN
BL-040-007 Harmoniser exceptions de rôle
BL-040-008 Ajouter JWK_ROTATION_REQUESTED
BL-040-009 Sécuriser metadata audit
BL-040-010 Harmoniser ports pour futures briques
BL-040-011 Ajouter tests anti-dépendances
BL-040-012 Documentation finale 0.4.0
```

---

## 15. Documentation

Créer ou compléter :

```text
docs/rbac.md
docs/security_rules.md
docs/audit.md
docs/ports.md
docs/integration_contracts.md
README.md
CHANGELOG.md
```

---

## 16. Critères de définition de terminé

`0.4.0` est terminée si :

- `DefaultAuthCatalog` existe et est exporté ;
- les 10 permissions existent ;
- les 4 rôles existent ;
- mapping conforme ;
- `ADMIN` ne peut pas gérer `SUPER_ADMIN` ;
- dernier `SUPER_ADMIN` protégé ;
- `JWK_ROTATION_REQUESTED` existe ;
- audit sans secret ;
- tests anti-dépendances OK ;
- documentation à jour ;
- `ruff`, `mypy`, `pytest` OK ;
- couverture ≥ 90 %.
