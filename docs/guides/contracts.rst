Contrats d'intégration par brique (v0.5.0)
==========================================

La v0.5.0 stabilise les contrats consommés par les briques aval. Chacun est
validé par un test dans ``tests/contracts/<brique>/`` n'important **que**
``baobab_auth_core``.

database
--------

Ports ``UserRepository``, ``RoleRepository``, ``PermissionRepository``,
``SessionRepository``, ``AuditRepository``, ``UnitOfWork``. ``DefaultAuthCatalog``
sert au seed ; le core ignore les noms de tables ; ``AuditEvent.metadata`` est
JSON-sérialisable ; les dates sont UTC aware.

security
--------

Ports ``PasswordHasher`` et ``TokenProvider`` ; DTO ``TokenIssueContext``,
``TokenClaims``, ``TokenPair``. Mapping : ``sub``=``AuthSubject``,
``jti``=``TokenId``, ``sid``=``SessionId``. Aucun JWT/Argon2 concret dans le core.

api
---

Un cas d'usage par endpoint (``RegisterUser`` → ``POST /auth/register``,
``GetCurrentUser`` → ``GET /auth/me``, etc.). Le core ne retourne jamais de
``HTTPException`` : il lève des exceptions ``BaobabAuthCoreError`` portant
``error_code`` / ``http_status`` (voir :doc:`error_codes`).

client
------

``AuthSubject``, ``AuthContext``, ``AuthenticatedUser``, ``TokenClaims``,
``RoleName``, ``PermissionName``. Le client **ne recalcule pas** les permissions :
``AuthContext`` et ``AuthenticatedUser`` les exposent directement.

admin
-----

``BootstrapSuperAdmin``, ``DisableUser``, ``EnableUser``, ``RequestJwkRotation``,
``ListRoles``, ``ListPermissions``, ``ListUserSessions``.
