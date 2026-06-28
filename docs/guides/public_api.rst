API publique (v0.5.0)
=====================

Le contrat public est l'ensemble des symboles exportés par
``baobab_auth_core.__all__``. Toute rupture (suppression / modification
incompatible) impose un bump SemVer **majeur** + note de migration.

Catégories exportées
--------------------

- **Entités** : ``User``, ``UserProfile``, ``Role``, ``Permission``, ``Session``,
  ``AuditEvent``.
- **Value objects** : ``Email``, ``AuthSubject``, ``PlainPassword``,
  ``PasswordHash``, ``RoleName``, ``PermissionName``, ``SessionId``, ``TokenId``,
  ``UserId``, ``RoleId``, ``PermissionId``, ``AuditEventId``.
- **Enums** : ``UserStatus``, ``SessionStatus``, ``AuditEventType``,
  ``AuditSeverity``.
- **Policies** : ``PasswordPolicy``, ``SessionPolicy``, ``RolePolicy``,
  ``PermissionPolicy``, ``LockoutPolicy``.
- **Catalogue** : ``DefaultAuthCatalog``.
- **Ports** : repositories (``User``/``Role``/``Permission``/``Session``/``Audit``),
  ``PasswordHasher``, ``TokenProvider``, ``Clock``, ``IdGenerator``, ``UnitOfWork``.
- **DTO** : ``AuthContext``, ``AuthenticatedUser``, ``TokenPair``, ``TokenClaims``,
  ``SessionDTO``, ``TokenIssueContext``.
- **Cas d'usage** : ``RegisterUser``, ``AuthenticateUser``, ``RefreshSession``,
  ``Logout``, ``RevokeSession``, ``RevokeAllSessions``, ``AssignRole``,
  ``RemoveRole``, ``ChangePassword``, ``DisableUser``, ``EnableUser``,
  ``BootstrapSuperAdmin``, ``RequestJwkRotation``, ``GetUserBySubject``,
  ``GetCurrentUser``, ``ListRoles``, ``ListPermissions``, ``ListUserSessions``.

Un test d'import (``tests/unit/baobab_auth_core/test_public_api.py``) garantit que
chaque symbole de ``__all__`` est réellement importable.
