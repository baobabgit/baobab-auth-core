# Contrat — API publique

> Ce fichier documente les symboles exportés dans `__all__` de ce package.
> Toute modification incompatible d'un symbole public déclenche un bump SemVer majeur.

## Symboles exportés

| Symbole | Type | Module | Spec |
|---------|------|--------|------|
| `__version__` | Constante | `baobab_auth_core` | BL-010-001 |
| `AuthContext` | DTO | `baobab_auth_core.application.results` | BL-030-001 |
| `AuthorizationService` | Service applicatif | `baobab_auth_core.application.services` | BL-030-002 |
| `AuditEvent` | Entité | `baobab_auth_core.domain.entities` | BL-010-003 |
| `Permission` | Entité | `baobab_auth_core.domain.entities` | BL-010-003 |
| `Role` | Entité | `baobab_auth_core.domain.entities` | BL-010-003 |
| `Session` | Entité | `baobab_auth_core.domain.entities` | BL-010-003 |
| `User` | Entité | `baobab_auth_core.domain.entities` | BL-010-003 |
| `UserProfile` | Entité | `baobab_auth_core.domain.entities` | BL-010-003 |
| `AuditEventType` | Enum | `baobab_auth_core.domain.enums` | BL-020-008 |
| `AuditSeverity` | Enum | `baobab_auth_core.domain.enums` | BL-020-008 |
| `SessionStatus` | Enum | `baobab_auth_core.domain.enums` | BL-010-004 |
| `UserStatus` | Enum | `baobab_auth_core.domain.enums` | BL-010-004 |
| `PasswordPolicy` | Policy | `baobab_auth_core.domain.policies` | BL-010-004 |
| `PermissionPolicy` | Policy | `baobab_auth_core.domain.policies` | BL-030-003 |
| `RolePolicy` | Policy | `baobab_auth_core.domain.policies` | BL-010-004 / BL-030-003 |
| `SessionPolicy` | Policy | `baobab_auth_core.domain.policies` | BL-010-004 |
| `AuditEventId` | Value object | `baobab_auth_core.domain.value_objects` | BL-020-008 |
| `AuthSubject` | Value object | `baobab_auth_core.domain.value_objects` | BL-010-002 |
| `Email` | Value object | `baobab_auth_core.domain.value_objects` | BL-010-002 |
| `PasswordHash` | Value object | `baobab_auth_core.domain.value_objects` | BL-010-002 |
| `PermissionId` | Value object | `baobab_auth_core.domain.value_objects` | BL-010-002 |
| `PermissionName` | Value object | `baobab_auth_core.domain.value_objects` | BL-010-002 / BL-030-003 |
| `PlainPassword` | Value object | `baobab_auth_core.domain.value_objects` | BL-010-002 |
| `RoleId` | Value object | `baobab_auth_core.domain.value_objects` | BL-010-002 |
| `RoleName` | Value object | `baobab_auth_core.domain.value_objects` | BL-010-002 |
| `SessionId` | Value object | `baobab_auth_core.domain.value_objects` | BL-010-002 |
| `TokenId` | Value object | `baobab_auth_core.domain.value_objects` | BL-020-002 |
| `UserId` | Value object | `baobab_auth_core.domain.value_objects` | BL-010-002 |
| `AuthorizationError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `BaobabAuthCoreError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `ForbiddenError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `InvalidCredentialsError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `InvalidEmailError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `InvalidPermissionNameError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `InvalidRoleNameError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `LastAdminRoleRemovalError` | Exception alias | `baobab_auth_core.exceptions` | BL-030-006 |
| `LastSuperAdminRoleRemovalError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 / BL-030-003 / BL-030-006 |
| `PermissionDeniedError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `PermissionNotFoundError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `RoleError` | Exception | `baobab_auth_core.exceptions` | BL-030-006 |
| `RoleNotFoundError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `SessionExpiredError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `SessionNotFoundError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `SessionRevokedError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `TokenExpiredError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `TokenInvalidError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `UserAlreadyExistsError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `UserDeletedError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `UserDisabledError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `UserLockedError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `UserNotFoundError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `ValidationError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `WeakPasswordError` | Exception | `baobab_auth_core.exceptions` | BL-010-005 |
| `AuditRepository` | Port | `baobab_auth_core.ports` | BL-020-008 |
| `Clock` | Port | `baobab_auth_core.ports` | BL-010-006 |
| `IdGenerator` | Port | `baobab_auth_core.ports` | BL-010-006 |
| `PasswordHasher` | Port | `baobab_auth_core.ports` | BL-010-006 |
| `PermissionRepository` | Port | `baobab_auth_core.ports` | BL-010-006 / BL-030-003 |
| `RoleRepository` | Port | `baobab_auth_core.ports` | BL-010-006 / BL-030-003 |
| `SessionRepository` | Port | `baobab_auth_core.ports` | BL-020-002 |
| `TokenProvider` | Port | `baobab_auth_core.ports` | BL-020-002 |
| `UnitOfWork` | Port | `baobab_auth_core.ports` | BL-020-001 |
| `UserRepository` | Port | `baobab_auth_core.ports` | BL-010-006 |
| `FakeClock` | Fake de test | `baobab_auth_core.testing` | BL-010-007 |
| `FakeIdGenerator` | Fake de test | `baobab_auth_core.testing` | BL-010-007 |
| `FakePasswordHasher` | Fake de test | `baobab_auth_core.testing` | BL-010-007 |
| `FakeTokenProvider` | Fake de test | `baobab_auth_core.testing` | BL-020-002 |
| `InMemoryAuditRepository` | Fake de test | `baobab_auth_core.testing` | BL-020-008 |
| `InMemoryPermissionRepository` | Fake de test | `baobab_auth_core.testing` | BL-010-007 / BL-030-003 |
| `InMemoryRoleRepository` | Fake de test | `baobab_auth_core.testing` | BL-010-007 / BL-030-003 |
| `InMemorySessionRepository` | Fake de test | `baobab_auth_core.testing` | BL-020-002 |
| `InMemoryUnitOfWork` | Fake de test | `baobab_auth_core.testing` | BL-020-001 |
| `InMemoryUserRepository` | Fake de test | `baobab_auth_core.testing` | BL-010-007 |

## Règle de rupture de contrat

- Suppression d'un symbole public → **MAJOR bump**
- Changement de signature incompatible → **MAJOR bump**
- Ajout d'un paramètre obligatoire → **MAJOR bump**
- Ajout d'un symbole → **MINOR bump**
- Correction de comportement sans rupture → **PATCH bump**
