Contrats d'intégration (v0.4.0)
===============================

``baobab-auth-core`` est une **librairie consommable** : ce qui est exporté dans
``baobab_auth_core.__all__`` et les signatures des ports constituent un **contrat**
versionné en SemVer.

Surface contractuelle
---------------------

- **Catalogue** : ``DefaultAuthCatalog`` (rôles, permissions, mapping) est une
  référence stable. Toute modification du mapping ou des noms est une rupture de
  contrat → bump majeur + note de migration.
- **Ports** (``typing.Protocol``) : ``PasswordHasher``, ``TokenProvider``,
  ``UserRepository``, ``RoleRepository``, ``PermissionRepository``,
  ``SessionRepository``, ``AuditRepository``, ``Clock``, ``IdGenerator``,
  ``UnitOfWork``. Le projet parent fournit les adaptateurs concrets.
- **Exceptions** : la hiérarchie publique (dont ``LastSuperAdminRoleRemovalError``
  et son alias ``LastAdminRoleRemovalError``) fait partie du contrat.

Responsabilités du projet parent
--------------------------------

- Implémenter les ports avec sa technologie (ORM, JWT, Argon2…) — jamais dans le core.
- Amorcer le RBAC à partir de ``DefaultAuthCatalog`` (persistance des rôles et
  permissions système).
- Brancher l'audit sur un ``AuditRepository`` concret ; ne jamais journaliser de
  secret (le ``AuditMetadataGuard`` du core rejette les clés sensibles).

Validation d'intégration
------------------------

La compatibilité inter-librairies se valide via git-ref sur la branche
``version/vX.Y.Z`` (voir ``docs/guides/how-to/integration-validation``) et la
matrice ``docs/integrations/compatibility_matrix.yaml``.
